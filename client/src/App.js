import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE_URL = 'http://localhost:8002';

function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [users, setUsers] = useState([]);
  const [posts, setPosts] = useState([]);
  const [newPost, setNewPost] = useState({ content: '', image_url: '' });
  const [newUser, setNewUser] = useState({
    username: '',
    email: '',
    full_name: '',
    bio: ''
  });
  const [loginUsername, setLoginUsername] = useState('');
  const [isLogin, setIsLogin] = useState(true);

  useEffect(() => {
    fetchUsers();
    fetchPosts();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/users/`);
      setUsers(response.data);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const fetchPosts = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/posts/`);
      setPosts(response.data);
    } catch (error) {
      console.error('Error fetching posts:', error);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.get(`${API_BASE_URL}/users/${loginUsername}`);
      setCurrentUser(response.data);
      setLoginUsername('');
    } catch (error) {
      alert('User not found!');
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API_BASE_URL}/users/`, newUser);
      setCurrentUser(response.data);
      setNewUser({ username: '', email: '', full_name: '', bio: '' });
      fetchUsers();
    } catch (error) {
      alert('Registration failed: ' + error.response?.data?.detail);
    }
  };

  const handleCreatePost = async (e) => {
    e.preventDefault();
    if (!currentUser) {
      alert('Please login first');
      return;
    }
    try {
      await axios.post(`${API_BASE_URL}/posts/?username=${currentUser.username}`, newPost);
      setNewPost({ content: '', image_url: '' });
      fetchPosts();
    } catch (error) {
      alert('Failed to create post: ' + error.response?.data?.detail);
    }
  };

  const handleLikePost = async (postId) => {
    if (!currentUser) {
      alert('Please login first');
      return;
    }
    try {
      await axios.post(`${API_BASE_URL}/likes/post/${postId}?username=${currentUser.username}`);
      fetchPosts();
    } catch (error) {
      console.error('Error liking post:', error);
    }
  };

  if (!currentUser) {
    return (
      <div className="app">
        <header className="header">
          <h1>🚀 Social Media App</h1>
        </header>

        <div className="auth-container">
          <div className="auth-tabs">
            <button
              className={isLogin ? 'tab active' : 'tab'}
              onClick={() => setIsLogin(true)}
            >
              Login
            </button>
            <button
              className={!isLogin ? 'tab active' : 'tab'}
              onClick={() => setIsLogin(false)}
            >
              Register
            </button>
          </div>

          {isLogin ? (
            <form onSubmit={handleLogin} className="auth-form">
              <input
                type="text"
                placeholder="Username"
                value={loginUsername}
                onChange={(e) => setLoginUsername(e.target.value)}
                required
              />
              <button type="submit">Login</button>
            </form>
          ) : (
            <form onSubmit={handleRegister} className="auth-form">
              <input
                type="text"
                placeholder="Username"
                value={newUser.username}
                onChange={(e) => setNewUser({...newUser, username: e.target.value})}
                required
              />
              <input
                type="email"
                placeholder="Email"
                value={newUser.email}
                onChange={(e) => setNewUser({...newUser, email: e.target.value})}
                required
              />
              <input
                type="text"
                placeholder="Full Name"
                value={newUser.full_name}
                onChange={(e) => setNewUser({...newUser, full_name: e.target.value})}
              />
              <textarea
                placeholder="Bio"
                value={newUser.bio}
                onChange={(e) => setNewUser({...newUser, bio: e.target.value})}
                rows="3"
              />
              <button type="submit">Register</button>
            </form>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🚀 Social Media App</h1>
        <div className="user-info">
          <span>Welcome, {currentUser.username}!</span>
          <button onClick={() => setCurrentUser(null)}>Logout</button>
        </div>
      </header>

      <div className="main-content">
        <div className="create-post">
          <h3>Create New Post</h3>
          <form onSubmit={handleCreatePost}>
            <textarea
              placeholder="What's on your mind?"
              value={newPost.content}
              onChange={(e) => setNewPost({...newPost, content: e.target.value})}
              required
              rows="3"
            />
            <input
              type="url"
              placeholder="Image URL (optional)"
              value={newPost.image_url}
              onChange={(e) => setNewPost({...newPost, image_url: e.target.value})}
            />
            <button type="submit">Share Post</button>
          </form>
        </div>

        <div className="posts-feed">
          <h3>Posts Feed</h3>
          {posts.length === 0 ? (
            <p>No posts yet. Be the first to post something!</p>
          ) : (
            posts.map(post => (
              <div key={post.element_id_property} className="post">
                <div className="post-header">
                  <strong>@{post.author_username || 'Unknown'}</strong>
                  <small>{new Date(post.created_at).toLocaleDateString()}</small>
                </div>
                <div className="post-content">
                  <p>{post.content}</p>
                  {post.image_url && (
                    <img src={post.image_url} alt="Post" className="post-image" />
                  )}
                </div>
                <div className="post-actions">
                  <button onClick={() => handleLikePost(post.element_id_property)}>
                    👍 {post.likes_count || 0}
                  </button>
                  <span>💬 {post.comments_count || 0}</span>
                </div>
              </div>
            ))
          )}
        </div>

        <div className="users-sidebar">
          <h3>Users ({users.length})</h3>
          {users.map(user => (
            <div key={user.element_id_property} className="user-item">
              <strong>@{user.username}</strong>
              {user.full_name && <p>{user.full_name}</p>}
              {user.bio && <p className="bio">{user.bio}</p>}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;