import * as React from 'react';
import { View, StyleSheet, Dimensions } from 'react-native';
import { TabView, TabBar, SceneMap } from 'react-native-tab-view';
import { Constants } from 'expo';
import MusicView from './Music';

const MusicRoute = () => (
  <MusicView />
);

const AlarmsRoute = () => (
  <View style={[styles.scene, { backgroundColor: '#673ab7' }]} />
);

export default class TabViewExample extends React.Component {
  state = {
    index: 0,
    routes: [
      { key: 'music', title: 'Music' },
      { key: 'alarms', title: 'Alarms' },
    ],
  };

  _handleIndexChange = index => this.setState({ index });

  _renderTabBar = props => <TabBar {...props} style={styles.header} />;

  _renderScene = SceneMap({
    music: MusicRoute,
    alarms: AlarmsRoute,
  });

  render() {
    return (
      <TabView
        navigationState={this.state}
        renderScene={this._renderScene}
        renderTabBar={this._renderTabBar}
        onIndexChange={this._handleIndexChange}
        initialLayout={{
          width: Dimensions.get('window').width,
        }}
      />
    );
  }
}

const styles = StyleSheet.create({
  scene: {
    flex: 1,
  },
  header: {
    paddingTop: Constants.statusBarHeight,
  },
});
