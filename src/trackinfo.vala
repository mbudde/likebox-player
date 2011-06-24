
public class Likebox.TrackInfo : GLib.Object {

    public string uri { get; set; }
    public string artist_name { get; set; }
    public string album_artist { get; set; }
    public string album_title { get; set; }
    public string track_title { get; set; }
    public string artwork_id { get; set; }
    public int track_number { get; set; }
    public int track_count { get; set; }
    public int year { get; set; }
    public int rating { get; set; }

}

public class Likebox.UnknownTrackInfo : TrackInfo {

    public UnknownTrackInfo (string uri) {
        this.uri = uri;
    }

}