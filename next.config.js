import MonacoWebpackPlugin from 'monaco-editor-webpack-plugin';

/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.plugins.push(
        new MonacoWebpackPlugin({
          languages: ['javascript', 'typescript', 'devscript'],
          filename: 'static/chunks/[name].worker.js',
          publicPath: '/_next'
        })
      );
    }
    return config;
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:5000/:path*',
      },
      {
        source: '/socket/:path*',
        destination: 'http://localhost:3001/:path*',
      },
    ]
  },
}

export default nextConfig
