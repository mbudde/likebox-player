
public class Likebox.PlayerEngine : GLib.Object {

    private Gst.Pipeline pipeline;
    private Gst.Element playbin;

    public signal void player_event (Event e);

    public PlayerEngine (string[] args) {
        Gst.init (ref args);

        pipeline = new Gst.Pipeline ("pipeline");
        playbin = Gst.ElementFactory.make ("playbin2", "playbin");
        pipeline.add (playbin);
        pipeline.set_state (Gst.State.READY);

        playbin.notify["volume"].connect ((s, e) => {
                player_event (Event.VOLUME);
            });
        pipeline.get_bus ().add_watch (parse_message);

        set_state (State.READY);
    }

    [Description(nick = "current track")]
    public TrackInfo current_track {
        get;
        private set;
    }

    [Description(nick = "current state of the engine")]
    public State current_state {
        get;
        private set;
    default = State.NOTREADY;
    }

    [Description(nick = "previous state of the engine")]
    public State previous_state {
        get;
        private set;
    default = State.NOTREADY;
    }

    [Description(nick = "volume")]
    public ushort volume {
        get {
            double volume;
            playbin.get ("volume", out volume);
            return (ushort) Math.lround (volume * 100.0);
        }
        set {
            double volume = Math.fmin (1.0, Math.fmax (0, value / 100.0));
            playbin.set ("volume", volume);
        }
    }

    private static Gst.Format query_format = Gst.Format.TIME;

    [Description(nick = "current position in the playing track")]
    public uint position {
        get {
            int64 pos;
            playbin.query_position (ref query_format, out pos);
            return (uint) (pos / Gst.MSECOND);
        }
        set {
            playbin.seek_simple (Gst.Format.TIME, Gst.SeekFlags.ACCURATE, (long)(value * Gst.MSECOND));
        }
    }

    [Description(nick = "length of current track")]
    public uint length {
        get {
            int64 duration;
            playbin.query_duration (ref query_format, out duration);
            return (uint) (duration / Gst.MSECOND);
        }
    }

    public void open_uri (string uri) {
        var track = new UnknownTrackInfo (uri);
        open_track (track);
    }

    /**
     * Opens the track for playing. Does not start playback.
     */
    public void open_track (TrackInfo track) {
        if (current_state == State.PLAYING || current_state == State.PAUSED) {
            pipeline.set_state (Gst.State.READY);
        }
        set_state (State.LOADING);
        playbin.set ("uri", track.uri);
        current_track = track;
    }

    public void close () {
        pipeline.set_state (Gst.State.NULL);
        set_state (State.IDLE);
    }

    public void reset () {
        current_track = null;
        close ();
        playbin.set ("uri", "");
    }

    public void play () {
        pipeline.set_state (Gst.State.PLAYING);
    }

    public void pause () {
        pipeline.set_state (Gst.State.PAUSED);
        set_state (State.PAUSED);
    }

    private void set_state (State state) {
        if (current_state == state) {
            return;
        }

        previous_state = current_state;
        current_state = state;
        player_event (Event.STATE_CHANGE);

        if (current_state == State.READY) {
            set_state (State.IDLE);
        }
    }

    private bool parse_message (Gst.Bus bus, Gst.Message message) {
        switch (message.type) {
        case Gst.MessageType.EOS:
            close ();
            player_event (Event.END_OF_STREAM);
            break;
        case Gst.MessageType.STATE_CHANGED:
            Gst.State old_state, new_state, pending_state;
            message.parse_state_changed (out old_state, out new_state, out pending_state);
            handle_state_change (old_state, new_state, pending_state);
            break;
        default:
            break;
        }
        return true;
    }

    private void handle_state_change (Gst.State old_state, Gst.State new_state, Gst.State pending_state) {
        if (current_state != State.LOADED && old_state == Gst.State.READY &&
            new_state == Gst.State.PAUSED && pending_state == Gst.State.PLAYING) {
            set_state (State.LOADED);
        } else if (old_state == Gst.State.PAUSED && new_state == Gst.State.PLAYING && pending_state == Gst.State.VOID_PENDING) {
            if (current_state == State.LOADED) {
                player_event (Event.START_OF_STREAM);
            }
            set_state (State.PLAYING);
        } else if (current_state == State.PLAYING && old_state == Gst.State.PLAYING && new_state == Gst.State.PAUSED) {
            set_state (State.PAUSED);
        }
    }

    public enum State {
        NOTREADY,
        READY,
        IDLE,
        LOADING,
        LOADED,
        PLAYING,
        PAUSED
    }

    public enum Event {
        NONE               = 0,
        ITERATE            = (1 << 1),
        STATE_CHANGE       = (1 << 2),
        START_OF_STREAM    = (1 << 3),
        END_OF_STREAM      = (1 << 4),
        BUFFERING          = (1 << 5),
        SEEK               = (1 << 6),
        ERROR              = (1 << 7),
        VOLUME             = (1 << 8),
        METADATA           = (1 << 9),
        TRACK_INFO_UPDATED = (1 << 10),
        REQUEST_NEXT_TRACK = (1 << 11),
    }

}
