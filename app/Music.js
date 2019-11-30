import React from 'react';
import {
  FlatList,
  Picker,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from 'react-native';
import { PI_URL } from './Config';


export default class Music extends React.Component {
  state = {
    text: '',
    results: [],
    wakeupSong: '',
    playlists: [],
    defaultPlaylist: null,
  };

  componentWillMount() {
    const headers = new Headers();
    headers.append("Accept", "application/json");
    fetch(PI_URL + '/spotify/next_wakeup_song').
      then(response => response.json()).
      then(wakeupSong => this.setState({ wakeupSong }));
    fetch(PI_URL + '/spotify/default_playlist').
      then(response => response.json()).
      then(defaultPlaylist => {
        if (defaultPlaylist) {
          this.setState({ defaultPlaylist: defaultPlaylist.uri })
        }
      });
    fetch(PI_URL + '/spotify/playlists').
      then(response => response.json()).
      then(playlists => this.setState({ playlists }));
  }

  searchSpotify = text => {
    this.setState({text});

    const headers = new Headers();
    headers.append("Accept", "application/json");
    fetch(PI_URL + '/spotify/search?q=' + encodeURI(text)).
      then(response => response.json()).
      then(json => this.setState({ results: json.tracks.items }));
  }

  selectSong = song_uri => {
    // find the song with that uri
    const track = this.state.results.find(t => t.uri === song_uri);

    const headers = new Headers();
    headers.append("Accept", "application/json");
    headers.append("Content-Type", "application/json");
    fetch(PI_URL + '/spotify/next_wakeup_song', {
      body: JSON.stringify(track),
      method: 'PUT',
      headers,
    }).
      then(response => response.json()).
      then(wakeupSong => {
        this.setState({
          results: [],
          text: '',
          wakeupSong,
        });
      });
  };

  selectDefaultPlaylist = playlistUri => {
    const playlist = this.state.playlists.find(p => p.uri === playlistUri);

    const headers = new Headers();
    headers.append("Accept", "application/json");
    headers.append("Content-Type", "application/json");
    fetch(PI_URL + '/spotify/default_playlist', {
      body: JSON.stringify({
        uri: playlist.uri,
        name: playlist.name,
      }),
      method: 'PUT',
      headers,
    }).
      then(response => response.json()).
      then(playlist => {
        this.setState({defaultPlaylist: playlist.uri})
      });
  };

  render() {
    return (
      <View style={[styles.scene]}>
        <TextInput
          placeholder="Search Spotify"
          style={{height: 40, borderColor: 'gray', borderWidth: 1}}
          onChangeText={this.searchSpotify}
          value={this.state.text} />
        { this.state.text ?
        <SongList data={ this.state.results } selectSong={ this.selectSong } />
        : null }
        <View>
          <Text>
            Wakeup Song: {this.state.wakeupSong ? this.state.wakeupSong.name + ' - ' + this.state.wakeupSong.artists[0].name : 'Not set'}
          </Text>
        </View>
        <View>
          <Text>
            Default Playlist:
          </Text>
        </View>
        <Picker
          selectedValue={ this.state.defaultPlaylist }
          onValueChange={ this.selectDefaultPlaylist }>
          { this.state.playlists.map(playlist => <Picker.Item key={ playlist.uri } label={ playlist.name } value={ playlist.uri } />) }
        </Picker>
      </View>
    );
  }
}

class SongItem extends React.PureComponent {
  _onPress = () => {
    this.props.onPressItem(this.props.id);
  };

  render() {
    return (
      <TouchableOpacity onPress={this._onPress} style={{minHeight: 40, padding: 20}}>
        <View>
          <Text>
            {this.props.title}
          </Text>
        </View>
        <View>
          <Text>
            {this.props.artist}
          </Text>
        </View>
      </TouchableOpacity>
    );
  }
}

class SongList extends React.PureComponent {
  _keyExtractor = (item, index) => item.id;

  _renderItem = ({item}) => (
    <SongItem
      id={item.uri}
      onPressItem={this.props.selectSong}
      title={item.name}
      artist={item.artists[0].name}
    />
  );

  render() {
    return (
      <FlatList
        data={this.props.data}
        keyExtractor={this._keyExtractor}
        renderItem={this._renderItem}
      />
    );
  }
}

const styles = StyleSheet.create({
  scene: {
    flex: 1,
    justifyContent: 'flex-start',
  },
});
