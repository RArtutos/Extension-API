import { storage } from './storage.js';
import { HeadersManager } from './http/headers.js';
import { RequestManager } from './http/request.js';
import { ErrorHandler } from './http/error.js';

class HttpClient {
  constructor() {
    this.errorHandler = new ErrorHandler();
    this.headersManager = new HeadersManager(() => storage.get('token'));
    this.requestManager = new RequestManager(this.headersManager, this.errorHandler);
  }

  get(endpoint) {
    return this.requestManager.makeRequest(endpoint);
  }

  post(endpoint, data) {
    return this.requestManager.makeRequest(endpoint, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  put(endpoint, data) {
    return this.requestManager.makeRequest(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  delete(endpoint) {
    return this.requestManager.makeRequest(endpoint, {
      method: 'DELETE'
    });
  }
}

export const httpClient = new HttpClient();