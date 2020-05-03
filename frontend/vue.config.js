module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  devServer: {
    disableHostCheck: true,
    public: 'gw2sdev-docker.ovh.net',
    proxy: {
      '/api/*': {
        target: process.env.VUE_APP_DEV_API_URL || ''
      }
    }
  }
};
