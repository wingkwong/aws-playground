import { Auth } from 'aws-amplify';

async function signUp() {
    try {
        const user = await Auth.signUp({
            username,
            password,
            attributes: {
                email,          // optional
                phone_number,   // optional - E.164 number convention
                // other custom attributes 
            }
        });
        console.log({ user });
        /*
            {
                user: CognitoUser;
                userConfirmed: boolean;
                userSub: string;
            }
        */
    } catch (error) {
        console.log('error signing up:', error);
    }
}

async function confirmSignUp() {
    try {
      await Auth.confirmSignUp(username, code);
    } catch (error) {
        console.log('error confirming sign up', error);
    }
}

async function signIn() {
    try {
        const user = await Auth.signIn(username, password);
    } catch (error) {
        console.log('error signing in', error);
    }
}

async function resendConfirmationCode() {
    try {
        await Auth.resendSignUp(username);
        console.log('code resent successfully');
    } catch (err) {
        console.log('error resending code: ', err);
    }
}

async function signOut() {
    try {
        await Auth.signOut();
    } catch (error) {
        console.log('error signing out: ', error);
    }
}

async function globalSignOut() {
    try {
        await Auth.signOut({ global: true });
    } catch (error) {
        console.log('error signing out: ', error);
    }
}

module.exports = {
    signUp,
    confirmSignUp,
    signIn,
    resendConfirmationCode,
    signOut,
    globalSignOut
};