import React, { useState } from 'react';
import { View, Text, FlatList, Button, StyleSheet } from 'react-native';

const initialPosts = [
  { id: '1', title: 'Welcome to EV Community', content: 'First post!', votes: 5, user: 'Anonymous' },
  { id: '2', title: 'Second Post', content: 'Electric vehicles are the future!', votes: 2, user: 'Alice' }
];

export default function App() {
  const [posts, setPosts] = useState(initialPosts);

  // handles the upvotes
  const handleUpvote = (id) => {
    setPosts(posts =>
      posts.map(post =>
        post.id === id ? { ...post, votes: post.votes + 1 } : post
      )
    );
  };

  // handles the downvotes
  const handleDownvote = (id) => {
    setPosts(posts =>
      posts.map(post =>
        post.id === id ? { ...post, votes: post.votes - 1 } : post
      )
    );
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>EV Community</Text>
      <FlatList
        data={posts.sort((a, b) => b.votes - a.votes)} 
        keyExtractor={item => item.id}
        renderItem={({ item }) => (
          <View style={styles.post}>
            <Text style={styles.title}>{item.title}</Text>
            <Text style={styles.content}>{item.content}</Text>
            <Text style={styles.meta}>Votes: {item.votes} | By: {item.user}</Text>
            <View style={styles.voteRow}>
              <Button title="Upvote" onPress={() => handleUpvote(item.id)} color="#FF5700"/>
              <View style={{ width: 16 }} />
              <Button title="Downvote" onPress={() => handleDownvote(item.id)} color="#7193FF"/>
            </View>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 22,
    paddingTop: 54,
    backgroundColor: '#f7f7f8',
    flex: 1,
  },
  header: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 24,
    color: '#FF5700', 
    alignSelf: 'center'
  },
  post: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 18,
    marginBottom: 18,
    shadowColor: '#000',
    shadowOpacity: 0.07,
    shadowRadius: 6,
    elevation: 2,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1a1a1b'
  },
  content: {
    fontSize: 15,
    marginVertical: 7,
    color: '#222'
  },
  meta: {
    fontSize: 13,
    color: '#6b7280',
    marginBottom: 7
  },
  voteRow: {
    flexDirection: 'row',
    marginTop: 8
  }
});
