export class ErrorHandler {
  static parseError(error) {
    if (error instanceof Response) {
      return this.parseResponseError(error);
    }
    
    if (error instanceof Error) {
      return error;
    }
    
    if (typeof error === 'object' && error.detail) {
      return new Error(error.detail);
    }
    
    return new Error('An unexpected error occurred');
  }

  static async parseResponseError(response) {
    try {
      const data = await response.json();
      return new Error(data.detail || 'Request failed');
    } catch {
      return new Error(`Request failed with status ${response.status}`);
    }
  }
}