import { useState } from 'react';
import { auth, db } from '../../config/firebase';
import { GoogleAuthProvider, signInWithPopup } from 'firebase/auth';
import { doc, setDoc, getDoc } from 'firebase/firestore';

interface GoogleAuthButtonProps {
  onLoginSuccess: (user: any) => void;
  onLoginFailure: (error: any) => void;
}
const GoogleAuthButton: React.FC<GoogleAuthButtonProps> = ({ onLoginSuccess, onLoginFailure }) => {
  const [authMessage, setAuthMessage] = useState('');

  const handleGoogleSignIn = async () => {
    try {
      const provider = new GoogleAuthProvider();
      const result = await signInWithPopup(auth, provider);
      const user = result.user;
      
      const userDoc = await getDoc(doc(db, 'users', user.uid));
      
      if (!userDoc.exists()) {
        await setDoc(doc(db, 'users', user.uid), {
          email: user.email,
          name: user.displayName,
          photoURL: user.photoURL,
          createdAt: new Date().toISOString(),
          authProvider: 'google',
          lastLogin: new Date().toISOString(),
          followers: [],
          following: [],
          publishedBots: [],
          publishedLibraries: [],
          publishedIdeas: []
        });
        setAuthMessage('Account created successfully!');
      } else {
        await setDoc(doc(db, 'users', user.uid), {
          lastLogin: new Date().toISOString()
        }, { merge: true });
        setAuthMessage('Welcome back!');
      }
      
      setTimeout(() => onLoginSuccess(user), 1500);
    } catch (error) {
      console.error('Google auth error:', error);
      onLoginFailure(error);
    }
  };

  return (
    <button onClick={handleGoogleSignIn} style={styles.googleButton}>
      <div style={styles.buttonContent}>
        <img 
          src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" 
          alt="Google"
          style={styles.googleIcon}
        />
        <span>Login with Google</span>
      </div>
    </button>
  );
};

const styles = {
  googleButton: {
    backgroundColor: '#ffffff',
    color: '#757575',
    padding: '12px 20px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '1em',
    width: '100%',
    transition: 'background-color 0.3s ease, transform 0.2s ease',
  },
  buttonContent: {
    display: 'flex' ,
    alignItems: 'center' ,
    justifyContent: 'center' ,
  },
  googleIcon: {
    width: '18px',
    height: '18px',
  }
};

export default GoogleAuthButton;
