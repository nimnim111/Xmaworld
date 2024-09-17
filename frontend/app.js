let auth0Client;

async function setupApp() {
    console.log('start');

    try {
        auth0Client = await createAuth0Client({
            domain: 'dev-rlt1xvwt50wj2dee.us.auth0.com',
            client_id: 'sqz00SEDvKB7pD96T8rRATrqgtIUdr26',
            redirect_uri: window.location.origin,
        });
        if (window.location.search.includes("code=") && window.location.search.includes("state=")) {
            console.log('got code');
            await auth0Client.handleRedirectCallback();
            await updateUI();
        }
        else{
         await auth0Client.loginWithRedirect();
         console.log('redirect');
         await updateUI();
        }

        // This function updates button visibility based on authentication status
        async function updateUI() {
            console.log("Hello world!"); 
            const isAuthenticated = await auth0Client.isAuthenticated();
            console.log('authenticated flag'+isAuthenticated); 
            if (isAuthenticated) {
                console.log ('success authentication');    
            }
            
        }

        // Check if the user is authenticated and update UI accordingly
       // await updateUI();

        
    } catch (error) {
        console.error("Error setting up authentication:", error);
    }
}

window.onload = setupApp;
