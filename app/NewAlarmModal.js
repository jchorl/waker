import React, {Component} from 'react';
import {Button, Modal, Switch, Text, TouchableHighlight, TouchableOpacity, View} from 'react-native';
import DateTimePicker from 'react-native-modal-datetime-picker';

export default class NewAlarmModal extends Component {
  state = {
    modalVisible: false,
    isDateTimePickerVisible: false,
    repeat: false,
    sunday: false,
    monday: false,
    tuesday: false,
    wednesday: false,
    thursday: false,
    friday: false,
    saturday: false,
  };

  setModalVisible(visible) {
    this.setState({modalVisible: visible});
  }

  _showDateTimePicker = () => this.setState({ isDateTimePickerVisible: true });

  _hideDateTimePicker = () => this.setState({ isDateTimePickerVisible: false });

  _handleTimePicked = time => {
    this.setState({ time });
    this._hideDateTimePicker();
  };

  newAlarm = () => {
    let days = this.state.repeat ? ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'].filter(a => this.state[a]) : undefined;
    this.props.newAlarm(this.state.time, this.state.repeat, days).then(() => {
      this.setModalVisible(false);
    });
  }

  render() {
    return (
      <View style={{marginTop: 22}}>
        <Modal
          animationType="slide"
          transparent={false}
          visible={this.state.modalVisible}
          onRequestClose={() => {
            alert('Modal has been closed.');
          }}>
          <View style={{marginTop: 22}}>
            <Text>New alarm</Text>
            <TouchableOpacity onPress={this._showDateTimePicker} style={{padding: 20}}>
              <Text>
              { this.state.time ? this.state.time.toLocaleTimeString() : 'Pick time' }
              </Text>
            </TouchableOpacity>
            <DateTimePicker
              isVisible={this.state.isDateTimePickerVisible}
              onConfirm={this._handleTimePicked}
              onCancel={this._hideDateTimePicker}
              mode="time"
            />
            <View style={{flexDirection: 'row', justifyContent: 'space-between'}}>
              <Text>
                Repeat
              </Text>
              <Switch value={this.state.repeat} onValueChange={repeat => this.setState({ repeat })} />
            </View>
            {this.state.repeat ? ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'].map(day => {
              return (
              <View style={{flexDirection: 'row', justifyContent: 'space-between'}} key={day}>
                <Text>
                  { day }
                </Text>
                <Switch value={this.state[day]} onValueChange={val => this.setState({ [day]: val })} />
              </View>
              );
            }) : null}
            <View style={{flexDirection: 'row', marginTop: 20}}>
              <View style={{flexGrow: 1, marginRight: 5}}>
                <Button title="Cancel" onPress={() => {
                  this.setModalVisible(!this.state.modalVisible);
                  }}
                />
              </View>
              <View style={{flexGrow: 1, marginLeft: 5}}>
                <Button title="Save" onPress={this.newAlarm}
                />
              </View>
            </View>
          </View>
        </Modal>

        <TouchableHighlight
          onPress={() => {
            this.setModalVisible(true);
          }}>
          <Text>New Alarm</Text>
        </TouchableHighlight>
      </View>
    );
  }
}
