
public class Likebox.Main : GLib.Object {

    public static int main(string[] args) {
        var engine = new PlayerEngine (args);
        var mainloop = new MainLoop ();

        engine.player_event.connect((s, e) => {
                if (e == PlayerEngine.PlayerEvent.END_OF_STREAM) {
                    stdout.printf ("Song ended\n");
                    stdout.flush ();
                    mainloop.quit ();
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

}
