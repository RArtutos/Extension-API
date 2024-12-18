export class ErrorHandler {
  async handle(error) {
    if (error.response?.data?.detail) {
      return new Error(error.response.data.detail);
    }
    if (error instanceof Response) {
      return await this.parseErrorResponse(error);
    }
    return new Error(error.message || 'An unexpected error occurred');
  }

  async parseErrorResponse(response) {
    try {
      const contentType = response.headers.get('content-type');
      if (contentType?.includes('application/json')) {
        const data = await response.json();
        return new Error(data.detail || data.message || 'Request failed');
      }
      return new Error('Request failed');
    } catch {
      return new Error('Request failed');
    }
  }
}