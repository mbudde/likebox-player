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

    public uint volume {
        get;
        set;
    }

    public uint position {
        get;
        set;
    }

    public uint length {
        get;
        private set;
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

    public void set_next_track (TrackInfo track) {
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
