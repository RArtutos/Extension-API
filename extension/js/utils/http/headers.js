export class HeadersManager {
  constructor(authTokenProvider) {
    this.authTokenProvider = authTokenProvider;
  }

  async getHeaders() {
    const token = await this.authTokenProvider();
    return {
      'Authorization': token ? `Bearer ${token}` : '',
      'Content-Type': 'application/json'
    };
  }
}