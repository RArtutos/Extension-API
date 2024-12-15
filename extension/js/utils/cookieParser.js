export function parseHeaderString(cookieString) {
  const cookies = [];
  const pairs = cookieString.split(';').map(pair => pair.trim());
  
  for (const pair of pairs) {
    if (!pair) continue;
    
    const [name, ...rest] = pair.split('=');
    const value = rest.join('='); // Por si el valor contiene '='
    
    if (name && value) {
      cookies.push({
        name: name.trim(),
        value: value.trim()
      });
    }
  }
  
  return cookies;
}