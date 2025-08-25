// API Error Handler - React/JavaScript
// This is my go-to error handling pattern for API calls

class ApiErrorHandler {
    static handle(error, context = 'API call') {
        // My philosophy: Always provide meaningful feedback to users
        // while logging detailed info for debugging
        
        console.error(`Error in ${context}:`, error);
        
        if (error.response) {
            // Server responded with error status
            const status = error.response.status;
            const message = error.response.data?.message || 'Server error';
            
            switch (status) {
                case 400:
                    return { 
                        userMessage: 'Please check your input and try again',
                        technical: message 
                    };
                case 401:
                    // Handle authentication
                    localStorage.removeItem('token');
                    window.location.href = '/login';
                    return { 
                        userMessage: 'Please log in again',
                        technical: 'Authentication failed' 
                    };
                case 403:
                    return { 
                        userMessage: 'You don\'t have permission for this action',
                        technical: message 
                    };
                case 500:
                    return { 
                        userMessage: 'Something went wrong on our end. Please try again later.',
                        technical: message 
                    };
                default:
                    return { 
                        userMessage: 'An unexpected error occurred',
                        technical: message 
                    };
            }
        } else if (error.request) {
            // Network error
            return {
                userMessage: 'Connection error. Please check your internet connection.',
                technical: 'Network error - no response received'
            };
        } else {
            // Other error
            return {
                userMessage: 'Something went wrong. Please try again.',
                technical: error.message
            };
        }
    }
}

// Usage example - this is how I typically structure API calls
async function fetchUserData(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        const errorInfo = ApiErrorHandler.handle(error, 'Fetching user data');
        
        // Show user-friendly message
        showNotification(errorInfo.userMessage, 'error');
        
        // Log for debugging
        console.error('Technical details:', errorInfo.technical);
        
        throw error; // Re-throw if needed by calling code
    }
}
