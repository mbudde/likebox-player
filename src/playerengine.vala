using Gst;

public class Likebox.PlayerEngine : GLib.Object {

    private Gst.Pipeline pipeline;
    private Gst.Element playbin;

    public signal void state_changed (PlayerState state);
    public signal void player_event (PlayerEvent e);

    public PlayerEngine (string[] args) {
        // Initializing GStreamer
        Gst.init (ref args);

        // Creating pipeline and elements
        pipeline = new Gst.Pipeline ("pipeline");
        playbin = ElementFactory.make ("playbin2", "playbin");
        pipeline.add (playbin);
        pipeline.set_state (Gst.State.READY);

        pipeline.get_bus ().add_watch (parse_message);

        current_state = PlayerState.READY;
    }

    public TrackInfo current_track {
        get;
        private set;
    }

    public PlayerState current_state {
        get;
        private set;
    default = PlayerState.NOTREADY;
    }

    public PlayerState last_state {
        get;
        private set;
    default = PlayerState.NOTREADY;
    }

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

    private static Format query_format = Gst.Format.TIME;
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

    public void open_track (TrackInfo track) {
        if (current_state == PlayerState.PLAYING || current_state == PlayerState.PAUSED) {
            pipeline.set_state (State.READY);
        }
        set_state (PlayerState.LOADING);
        playbin.set ("uri", track.uri);
        current_track = track;
    }

    public void close () {
        pipeline.set_state (State.NULL);
        set_state (PlayerState.READY);
    }

    public void play () {
        pipeline.set_state (State.PLAYING);
        set_state (PlayerState.PLAYING);
    }

    public void pause () {
        pipeline.set_state (State.PAUSED);
        set_state (PlayerState.PAUSED);
    }

    protected void set_state (PlayerState state) {
        if (current_state == state) {
            return;
        }

        last_state = current_state;
        current_state = state;
        state_changed (state);
    }

    private bool parse_message (Gst.Bus bus, Gst.Message message) {
        switch (message.type) {
        case Gst.MessageType.EOS:
            close ();
            player_event (PlayerEvent.END_OF_STREAM);
            break;
        case Gst.MessageType.STATE_CHANGED:
            break;
        default:
            break;
        }
        return true;
    }

    public enum PlayerState {
        NOTREADY,
        READY,
        IDLE,
        LOADING,
        LOADED,
        PLAYING,
        PAUSED
    }

    public enum PlayerEvent {
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
