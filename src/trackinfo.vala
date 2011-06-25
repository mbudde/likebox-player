//
// trackinfo.vala - part of likebox-player
//
// Copyright (C) 2011 Michael Budde <mbudde@gmail.com>
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.
//

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