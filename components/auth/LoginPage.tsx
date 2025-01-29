import React, { useState, useEffect } from 'react';
import PhoneInput from 'react-phone-input-2';
import 'react-phone-input-2/lib/style.css';
import AuthButton from './AuthButton';
import GoogleAuthButton from './GoogleAuthButton';
import Image from 'next/image';
import { auth, db } from '../../config/firebase';
import { createUserWithEmailAndPassword, signInWithEmailAndPassword, fetchSignInMethodsForEmail } from 'firebase/auth';
import { doc, setDoc, getDoc } from 'firebase/firestore';

interface LoginPageProps {
    onLogin: (user: any) => void;
}

const LoginPage: React.FC<LoginPageProps> = ({ onLogin }) => {
    const [isSignUp, setIsSignUp] = useState(false);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [username, setUsername] = useState('');
    const [name, setName] = useState('');
    const [slide, setSlide] = useState(false);
    const [passwordError, setPasswordError] = useState('');
    const [emailError, setEmailError] = useState('');
    const [isPasswordValid, setIsPasswordValid] = useState(false);
    const [isEmailValid, setIsEmailValid] = useState(false);
    const [isPhoneValid, setIsPhoneValid] = useState(false);

    const validateEmail = async (email: string) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const isValidFormat = emailRegex.test(email);
        
        if (!isValidFormat) {
            setEmailError('Invalid email format');
            setIsEmailValid(false);
            return;
        }

        try {
            const signInMethods = await fetchSignInMethodsForEmail(auth, email);
            if (isSignUp && signInMethods.length > 0) {
                setEmailError('Email already registered');
                setIsEmailValid(false);
            } else {
                setEmailError('');
                setIsEmailValid(true);
            }
        } catch (error) {
            setEmailError('Error checking email');
            setIsEmailValid(false);
        }
    };

    const validatePassword = (password: string) => {
        const minLength = password.length >= 8;
        const hasUpperCase = /[A-Z]/.test(password);
        const hasLowerCase = /[a-z]/.test(password);
        const hasNumber = /[0-9]/.test(password);
        const hasSymbol = /[!@#$%^&*(),.?":{}|<>]/.test(password);

        const isValid = minLength && hasUpperCase && hasLowerCase && hasNumber && hasSymbol;
        setIsPasswordValid(isValid);

        if (!minLength) return "Password must be at least 8 characters";
        if (!hasUpperCase) return "Password must include an uppercase letter";
        if (!hasLowerCase) return "Password must include a lowercase letter";
        if (!hasNumber) return "Password must include a number";
        if (!hasSymbol) return "Password must include a symbol";
        return "";
    }

    const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const newPassword = e.target.value;
        setPassword(newPassword);
        setPasswordError(validatePassword(newPassword));
    };

    const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const newEmail = e.target.value;
        setEmail(newEmail);
        validateEmail(newEmail);
    };

    const handleToggleSlide = () => {
        setSlide(!slide);
        setIsSignUp(!isSignUp);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        
        if (!isEmailValid || !isPasswordValid || (isSignUp && !isPhoneValid)) {
            return;
        }

        try {
            if (isSignUp) {
                const userCredential = await createUserWithEmailAndPassword(auth, email, password);
                const user = userCredential.user;
                
                await setDoc(doc(db, 'users', user.uid), {
                    email,
                    username,
                    name,
                    phoneNumber,
                    createdAt: new Date().toISOString(),
                    authProvider: 'email',
                    lastLogin: new Date().toISOString()
                });
                
                onLogin(user);
            } else {
                const userCredential = await signInWithEmailAndPassword(auth, email, password);
                await setDoc(doc(db, 'users', userCredential.user.uid), {
                    lastLogin: new Date().toISOString()
                }, { merge: true });
                
                onLogin(userCredential.user);
            }
        } catch (error: any) {
            console.error('Authentication error:', error.message);
        }
    };

    return (
        <div style={styles.container}>
            <div style={{
                ...styles.splitSection,
                transform: slide ? 'translateX(100%)' : 'translateX(0)',
                left: 0
            }}>
                <div style={styles.formContainer}>
                    {!isSignUp && <h1 style={styles.welcomeText}>WELCOME BACK</h1>}
                    <h2 style={styles.title}>{isSignUp ? 'Create Account' : 'Login'}</h2>
                    <div style={styles.inputGroup}>
                        <label style={styles.inputLabel}>EMAIL ADDRESS</label>
                        <input
                            type="email"
                            value={email}
                            onChange={handleEmailChange}
                            style={styles.input}
                        />
                        {emailError && <div style={styles.errorText}>{emailError}</div>}
                        
                        {isSignUp && (
                            <>
                                <label style={styles.inputLabel}>USERNAME</label>
                                <input
                                    type="text"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    style={styles.input}
                                />
                                <label style={styles.inputLabel}>FULL NAME</label>
                                <input
                                    type="text"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    style={styles.input}
                                />
                                <label style={styles.inputLabel}>PHONE NUMBER</label>
                                <PhoneInput
                                    country={'us'}
                                    value={phoneNumber}
                                    onChange={(phone) => {
                                        setPhoneNumber(phone);
                                        setIsPhoneValid(phone.length >= 10);
                                    }}
                                    containerStyle={{ width: '100%' }}
                                    inputStyle={{
                                        width: '100%',
                                        height: '35px',
                                        fontSize: '14px',
                                        backgroundColor: '#333',
                                        border: 'none',
                                        color: '#fff'
                                    }}
                                    buttonStyle={{
                                        backgroundColor: '#333',
                                        border: 'none',
                                        padding: '0 5px'
                                    }}
                                />
                            </>
                        )}
                        <label style={styles.inputLabel}>PASSWORD</label>
                        <input
                            type="password"
                            value={password}
                            onChange={handlePasswordChange}
                            style={styles.input}
                        />
                        <div style={styles.passwordRequirements}>
                            {passwordError && <span style={styles.errorText}>{passwordError}</span>}
                        </div>
                    </div>
                    <button 
                        style={{
                            ...styles.loginButton,
                            opacity: (isEmailValid && isPasswordValid && (!isSignUp || isPhoneValid)) ? 1 : 0.6,
                            cursor: (isEmailValid && isPasswordValid && (!isSignUp || isPhoneValid)) ? 'pointer' : 'not-allowed'
                        }}
                        onClick={handleSubmit}
                        disabled={!(isEmailValid && isPasswordValid && (!isSignUp || isPhoneValid))}
                    >
                        {isSignUp ? 'Sign Up' : 'Login'}
                    </button>
                    <div style={styles.separator}>
                        <hr style={styles.separatorLine} />
                        <span style={styles.separatorText}>or</span>
                        <hr style={styles.separatorLine} />
                    </div>
                    <GoogleAuthButton 
                        onLoginSuccess={onLogin}
                        onLoginFailure={(error) => console.error(error)}
                    />
                </div>
            </div>
            <div style={{
                ...styles.splitSection,
                transform: slide ? 'translateX(-100%)' : 'translateX(0)',
                right: 0,
                height: '100vh',
                display: 'flex',
                alignItems: 'stretch'
            }} onClick={handleToggleSlide}>
                <div style={styles.imageContainer}>
                    <Image
                        src="/twack1.33.png"
                        alt="Login Art"
                        priority
                        quality={100}
                        fill
                        style={{
                            objectFit: 'contain',
                            height: '100%',
                            maxWidth: '100%',
                        }}
                    />
                </div>
            </div>
        </div>
    );
};

const styles = {
    container: {
        display: 'flex',
        width: 'calc(100vw - 40px)',
        height: '100vh',
        position: 'relative',
        overflow: 'hidden',
        backgroundColor: '#1A1A1A',
    },
    splitSection: {
        position: 'absolute',
        width: '50%',
        height: '100%',
        transition: 'transform 0.6s ease-in-out',
    },
    formContainer: {
        padding: '20px',
        maxWidth: '350px',
        margin: '0 auto',
        display: 'flex',
        flexDirection: 'column' ,
        justifyContent: 'center',
        height: '100%',
        gap: '10px'
    },
    welcomeText: {
        color: '#fff',
        fontSize: '2em',
        fontWeight: 'bold',
        marginBottom: '10px',
        letterSpacing: '2px',
    },
    title: {
        color: '#fff',
        fontSize: '1.5em',
        marginBottom: '20px',
    },
    inputLabel: {
        color: '#fff',
        fontSize: '0.8em',
        fontWeight: 'bold',
        marginBottom: '8px',
        letterSpacing: '1px',
    },
    inputGroup: {
        marginBottom: '10px',
    },
    input: {
        width: '100%',
        padding: '8px',
        backgroundColor: '#333',
        border: 'none',
        borderRadius: '4px',
        color: '#fff',
        marginBottom: '10px',
    },
    loginButton: {
        width: '100%',
        padding: '12px',
        backgroundColor: '#2a2a2a',
        color: '#fff',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        fontSize: '1em',
        transition: 'background-color 0.3s ease',
    },
    separator: {
        display: 'flex',
        alignItems: 'center',
        margin: '20px 0',
    },
    separatorLine: {
        flex: 1,
        height: '1px',
        backgroundColor: '#444',
        border: 'none',
    },
    separatorText: {
        color: '#666',
        padding: '0 10px',
    },
    imageContainer: {
        position: 'relative',
        width: '100%',
        height: '100%',
    },
    passwordRequirements: {
        fontSize: '0.8em',
        color: '#ff4444',
        marginTop: '-8px',
        marginBottom: '10px'
    },
    errorText: {
        color: '#ff4444',
        fontSize: '0.8em'
    },
    phoneInput: {
        marginBottom: '10px',
        '& .react-phone-input': {
            width: '100%'
        }
    }
};

export default LoginPage;
