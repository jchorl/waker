import * as React from 'react';
import { View, StyleSheet, Dimensions } from 'react-native';
import { TabView, TabBar, SceneMap } from 'react-native-tab-view';
import { Constants } from 'expo';
import MusicView from './Music';
import AlarmView from './Alarm';

const MusicRoute = () => (
  <MusicView />
);

const AlarmsRoute = () => (
  <AlarmView />
);

export default class App extends React.Component {
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
  header: {
    paddingTop: Constants.statusBarHeight,
  },
});
