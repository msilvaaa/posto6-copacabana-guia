// Route only posto6copacabana.com.br/guia* to this Worker.
// The existing DNS origin continues serving every other path.
export const UPSTREAM = 'https://posto6-copacabana-guia.pages.dev';
export const PREFIX = '/guia';
export function localPath(path) {
  return path.startsWith('/') && !path.startsWith('//') && path !== PREFIX && !path.startsWith(PREFIX + '/') ? PREFIX + path : path;
}
export function rewriteText(text) {
  // Root-relative HTML attributes, JS strings/template literals, JSON and CSS strings.
  text = text.replaceAll(UPSTREAM + '/', '/');
  text = text.replace(/(["'`])\/(?!\/)([^"'`\r\n]*?)\1/g, (_, quote, rest) => quote + localPath('/' + rest) + quote);
  // Unquoted CSS resource references.
  text = text.replace(/url\(\s*(\/[^\s)'"`]+)\s*\)/g, (_, path) => 'url(' + localPath(path) + ')');
  text = text.replace(/\bsrcset=("|')([^"']*)\1/gi, (_, quote, value) => 'srcset=' + quote + value.split(',').map(part => part.replace(/^(\s*)(\/\S+)/, (_, space, path) => space + localPath(path))).join(',') + quote);
  return text;
}
export async function handle(request, fetcher = fetch) {
  const url = new URL(request.url);
  if (url.pathname !== PREFIX && !url.pathname.startsWith(PREFIX + '/')) return fetcher(request);
  if (url.pathname === PREFIX) {
    url.pathname += '/';
    return Response.redirect(url.href, 308);
  }
  const target = new URL(url.pathname.slice(PREFIX.length) + url.search, UPSTREAM);
  const headers = new Headers(request.headers);
  // Guest-guide upstream is public; do not forward cookies/credentials from the old project.
  for (const name of ['host', 'cookie', 'authorization']) headers.delete(name);
  let upstream;
  try {
    upstream = await fetcher(new Request(target, {method:request.method, headers, redirect:'manual', body:['GET','HEAD'].includes(request.method) ? undefined : request.body}));
  } catch {
    return new Response('Guia temporariamente indisponível. Tente novamente.', {status:502});
  }
  const responseHeaders = new Headers(upstream.headers);
  responseHeaders.delete('set-cookie');
  const location = responseHeaders.get('location');
  if (location) {
    const destination = new URL(location, target);
    if (destination.origin === UPSTREAM) responseHeaders.set('location', url.origin + localPath(destination.pathname) + destination.search + destination.hash);
  }
  const type = responseHeaders.get('content-type') || '';
  if (request.method !== 'HEAD' && /text\/|javascript|json|svg\+xml/i.test(type)) {
    const body = rewriteText(await upstream.text());
    for (const name of ['content-length','content-encoding','etag','content-md5']) responseHeaders.delete(name);
    return new Response(body, {status:upstream.status, headers:responseHeaders});
  }
  return new Response(upstream.body, {status:upstream.status, headers:responseHeaders});
}
export default {fetch(request) { return handle(request); }};
