import React from 'react';
import {
  Button,
  FlatList,
  StyleSheet,
  Text,
  View,
} from 'react-native';
import { PI_URL } from './Config';
import NewAlarmModal from './NewAlarmModal';

function compareTimes(a, b) {
  if (a.time.hour < b.time.hour || a.time.hour === b.time.hour && a.time.minute < b.time.minute) {
    return -1;
  }
  if (a.time.hour > b.time.hour || a.time.hour === b.time.hour && a.time.minute > b.time.minute) {
    return 1;
  }
  return 0;
}

export default class AlarmView extends React.Component {
  state = {
    alarms: [],
  };

  componentWillMount() {
    const headers = new Headers();
    headers.append("Accept", "application/json");
    fetch(PI_URL + '/alarms').
      then(response => response.json()).
      then(alarms => {
        alarms.sort(compareTimes);
        this.setState({ alarms })
      });
  }

  newAlarm = (time, repeat, days) => {
    const headers = new Headers();
    headers.append("Accept", "application/json");
    headers.append("Content-Type", "application/json");
    return fetch(PI_URL + '/alarms', {
      body: JSON.stringify({
        time: {
          hour: time.getUTCHours(),
          minute: time.getUTCMinutes(),
        },
        repeat,
        days,
      }),
      method: 'POST',
      headers,
    }).
      then(response => response.json()).
      then(alarm => {
        let alarms = this.state.alarms.slice(0);
        alarms.push(alarm);
        alarms.sort(compareTimes);
        this.setState({
          alarms,
        });
      });
  }

  deleteAlarm = id => {
    const headers = new Headers();
    headers.append("Accept", "application/json");
    fetch(PI_URL + '/alarms/' + id, {
      method: 'DELETE',
      headers,
    }).
      then(response => response.text()).
      then(id => {
        let alarms = this.state.alarms.slice(0).filter(a => a.id !== id);
        this.setState({
          alarms,
        });
      });
  };

  render() {
    return (
      <View>
        <NewAlarmModal newAlarm={ this.newAlarm } />
        <AlarmList alarms={this.state.alarms} deleteAlarm={this.deleteAlarm} />
      </View>
    );
  }
}

class AlarmItem extends React.PureComponent {
  zeroPad = num => num < 10 ? '0' + num : '' + num;

  deleteAlarm = id => () => this.props.deleteAlarm(id);

  render() {
    const time = new Date();
    time.setUTCHours(this.props.time.hour);
    time.setUTCMinutes(this.props.time.minute);
    return (
      <View style={{minHeight: 40, padding: 20, borderWidth: 1, borderColor: '#000'}}>
        <View style={{flexDirection: 'row', justifyContent: 'space-between'}}>
          <Text>
            {this.zeroPad(time.getHours()) + ':' + this.zeroPad(time.getMinutes())}
          </Text>
          <Text>
            {this.props.repeat ? this.props.days.join(', ') : ''}
          </Text>
        </View>
        <Text>
          Next run: {this.props.nextRun.toLocaleString()}
        </Text>
        <Button title="Delete" onPress={this.deleteAlarm(this.props.id)} />
      </View>
      );
  }
}

class AlarmList extends React.PureComponent {
  _keyExtractor = (alarm, index) => alarm.id;

  _renderItem = ({item}) => {
    return (
      <AlarmItem
        id={item.id}
        time={item.time}
        repeat={item.repeat}
        days={item.days}
        nextRun={new Date(item.next_run)}
        deleteAlarm={this.props.deleteAlarm}
      />
      )
  };

  render() {
    return (
      <FlatList
        data={this.props.alarms}
        keyExtractor={this._keyExtractor}
        renderItem={this._renderItem}
      />
    );
  }
}
