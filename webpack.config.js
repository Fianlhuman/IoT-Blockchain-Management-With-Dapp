const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const CopyPlugin = require('copy-webpack-plugin');

const DIST = path.resolve(__dirname, 'dist');

module.exports = {
  devtool: 'eval-source-map',
  mode: 'development',
  entry: './src/assets/js/index.js',
  output: {
    filename: 'assets/js/bundle.js',
    path: DIST,
    publicPath: DIST,
  },
  devServer: {
    contentBase: DIST,
    port: 9011,
    writeToDisk: true,
  },
  plugins: [
    new CleanWebpackPlugin({ cleanStaleWebpackAssets: false }),

    // for build scripts
    new CopyPlugin({
      patterns: [
        {
          flatten: true,
          from: './src/*',
          globOptions: {
            ignore: ['**/*.js'],
          },
        },
        {
          flatten: false,
          from: './src/assets/',
          to: 'assets/',
          globOptions: {
          },
        },
      ],
    }),
    // generate HTML file with bundle.js injected
  ],
};
