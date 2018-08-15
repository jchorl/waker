import React from 'react';
import { FlatList, View, StyleSheet, Text, TextInput, TouchableOpacity } from 'react-native';
import { PI_URL } from './Config';


export default class Music extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      text: '',
      results: [],
      wakeupSong: '',
    };
  }

  componentWillMount() {
    const headers = new Headers();
    headers.append("Accept", "application/json");
    fetch(PI_URL + '/spotify/next_wakeup_song').
      then(response => response.json()).
      then(wakeupSong => this.setState({ wakeupSong }));
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
      body: JSON.stringify({
        uri: track.uri,
        name: track.name,
        artist: track.artists[0].name,
      }),
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
            Wakeup Song: {this.state.wakeupSong ? this.state.wakeupSong.name + ' - ' + this.state.wakeupSong.artist : 'Not set'}
          </Text>
        </View>
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
