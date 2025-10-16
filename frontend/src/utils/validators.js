/**
 * Validate query input
 */
export const validateQuery = (query) => {
  if (!query || typeof query !== 'string') {
    return { valid: false, error: 'Query is required' };
  }

  const trimmed = query.trim();

  if (trimmed.length === 0) {
    return { valid: false, error: 'Query cannot be empty' };
  }

  if (trimmed.length < 3) {
    return { valid: false, error: 'Query must be at least 3 characters' };
  }

  if (trimmed.length > 1000) {
    return { valid: false, error: 'Query must be less than 1000 characters' };
  }

  return { valid: true, error: null };
};

/**
 * Validate client ID
 */
export const validateClientId = (clientId) => {
  if (!clientId || typeof clientId !== 'string') {
    return { valid: false, error: 'Client ID is required' };
  }

  const pattern = /^CLT-\d{3}$/;
  if (!pattern.test(clientId)) {
    return { valid: false, error: 'Invalid client ID format' };
  }

  return { valid: true, error: null };
};

/**
 * Validate session ID
 */
export const validateSessionId = (sessionId) => {
  if (!sessionId || typeof sessionId !== 'string') {
    return { valid: false, error: 'Session ID is required' };
  }

  if (sessionId.length < 10) {
    return { valid: false, error: 'Invalid session ID' };
  }

  return { valid: true, error: null };
};

/**
 * Validate email
 */
export const validateEmail = (email) => {
  if (!email || typeof email !== 'string') {
    return { valid: false, error: 'Email is required' };
  }

  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!pattern.test(email)) {
    return { valid: false, error: 'Invalid email format' };
  }

  return { valid: true, error: null };
};

/**
 * Sanitize user input
 */
export const sanitizeInput = (input) => {
  if (typeof input !== 'string') return '';

  // Remove potential XSS patterns
  return input
    .replace(/<script[^>]*>.*?<\/script>/gi, '')
    .replace(/<iframe[^>]*>.*?<\/iframe>/gi, '')
    .replace(/javascript:/gi, '')
    .replace(/on\w+\s*=/gi, '');
};

/**
 * Check if value is empty
 */
export const isEmpty = (value) => {
  if (value === null || value === undefined) return true;
  if (typeof value === 'string') return value.trim().length === 0;
  if (Array.isArray(value)) return value.length === 0;
  if (typeof value === 'object') return Object.keys(value).length === 0;
  return false;
};

/**
 * Validate number range
 */
export const validateNumberRange = (value, min, max) => {
  if (typeof value !== 'number' || isNaN(value)) {
    return { valid: false, error: 'Value must be a number' };
  }

  if (value < min) {
    return { valid: false, error: `Value must be at least ${min}` };
  }

  if (value > max) {
    return { valid: false, error: `Value must be at most ${max}` };
  }

  return { valid: true, error: null };
};

/**
 * Validate API response
 */
export const validateApiResponse = (response) => {
  if (!response) {
    return { valid: false, error: 'Empty response' };
  }

  if (typeof response !== 'object') {
    return { valid: false, error: 'Invalid response format' };
  }

  return { valid: true, error: null };
};
