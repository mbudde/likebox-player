
public class Likebox.Main : GLib.Object {

    public static int main(string[] args) {
        var engine = new PlayerEngine (args);
        var mainloop = new MainLoop ();

        Log.set_handler (null, LogLevelFlags.LEVEL_WARNING | LogLevelFlags.FLAG_FATAL
                   | LogLevelFlags.FLAG_RECURSION, log_handler);

        engine.player_event.connect((s, e) => {
                switch (e) {
                case PlayerEngine.PlayerEvent.END_OF_STREAM:
                    mainloop.quit ();
                    break;
                case PlayerEngine.PlayerEvent.VOLUME:
                    stdout.printf ("volume: %u\n", engine.volume);
                    stdout.flush ();
                    break;
                }
            });

        if (args.length <= 1) {
            stdout.printf("Missing filename\n");
            return 1;
        }

        var uri = Filename.to_uri (args[1]);
        var track = new UnknownTrackInfo (uri);
        engine.open_track (track);
        engine.play ();
        mainloop.run ();
        return 0;
    }

    public static void log_handler (string? log_domain, LogLevelFlags log_levels, string message) {
        stderr.printf (message);
    }

}
