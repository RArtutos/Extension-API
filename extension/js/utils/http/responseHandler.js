export class ResponseHandler {
  static async handle(response) {
    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('authentication_required');
      }
      
      const contentType = response.headers.get('content-type');
      if (contentType?.includes('application/json')) {
        const error = await response.json();
        throw new Error(error.detail || 'Request failed');
      }
      
      throw new Error(`Request failed with status ${response.status}`);
    }

    if (response.status === 204) {
      return true;
    }

    return response.json();
  }
}