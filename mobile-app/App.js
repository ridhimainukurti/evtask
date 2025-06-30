import React from 'react';
import { View, Text, FlatList } from 'react-native';

const DATA = [
  { id: '1', title: 'Welcome to EV Community', content: 'First post!', votes: 5 },
];

const App = () => (
  <View style={{ padding: 20 }}>
    <Text style={{ fontSize: 24 }}>EV Community</Text>
    <FlatList
      data={DATA}
      keyExtractor={item => item.id}
      renderItem={({ item }) => (
        <View style={{ marginVertical: 10 }}>
          <Text style={{ fontWeight: 'bold' }}>{item.title}</Text>
          <Text>{item.content}</Text>
          <Text>Votes: {item.votes}</Text>
        </View>
      )}
    />
  </View>
);

export default App;
