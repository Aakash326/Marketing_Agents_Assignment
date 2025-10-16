/**
 * Storage service for managing localStorage operations
 */

const STORAGE_KEYS = {
  THEME: 'theme',
  SELECTED_CLIENT: 'selectedClient',
  SESSION_PREFIX: 'session_',
  CONVERSATION_PREFIX: 'conversation_',
  USER_PREFERENCES: 'userPreferences'
};

export const storageService = {
  // Theme
  getTheme: () => localStorage.getItem(STORAGE_KEYS.THEME),
  setTheme: (theme) => localStorage.setItem(STORAGE_KEYS.THEME, theme),

  // Client
  getSelectedClient: () => localStorage.getItem(STORAGE_KEYS.SELECTED_CLIENT),
  setSelectedClient: (clientId) => localStorage.setItem(STORAGE_KEYS.SELECTED_CLIENT, clientId),

  // Session
  getSession: (clientId) => {
    const key = `${STORAGE_KEYS.SESSION_PREFIX}${clientId}`;
    return localStorage.getItem(key);
  },
  setSession: (clientId, sessionId) => {
    const key = `${STORAGE_KEYS.SESSION_PREFIX}${clientId}`;
    localStorage.setItem(key, sessionId);
  },
  removeSession: (clientId) => {
    const key = `${STORAGE_KEYS.SESSION_PREFIX}${clientId}`;
    localStorage.removeItem(key);
  },

  // Conversation History
  getConversation: (sessionId) => {
    const key = `${STORAGE_KEYS.CONVERSATION_PREFIX}${sessionId}`;
    const data = localStorage.getItem(key);
    return data ? JSON.parse(data) : [];
  },
  setConversation: (sessionId, messages) => {
    const key = `${STORAGE_KEYS.CONVERSATION_PREFIX}${sessionId}`;
    localStorage.setItem(key, JSON.stringify(messages));
  },
  removeConversation: (sessionId) => {
    const key = `${STORAGE_KEYS.CONVERSATION_PREFIX}${sessionId}`;
    localStorage.removeItem(key);
  },

  // User Preferences
  getPreferences: () => {
    const data = localStorage.getItem(STORAGE_KEYS.USER_PREFERENCES);
    return data ? JSON.parse(data) : {};
  },
  setPreferences: (preferences) => {
    localStorage.setItem(STORAGE_KEYS.USER_PREFERENCES, JSON.stringify(preferences));
  },
  updatePreference: (key, value) => {
    const prefs = storageService.getPreferences();
    prefs[key] = value;
    storageService.setPreferences(prefs);
  },

  // Clear all data
  clearAll: () => {
    localStorage.clear();
  },

  // Clear specific client data
  clearClientData: (clientId) => {
    storageService.removeSession(clientId);
    const sessionId = storageService.getSession(clientId);
    if (sessionId) {
      storageService.removeConversation(sessionId);
    }
  }
};
