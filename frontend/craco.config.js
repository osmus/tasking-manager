module.exports = {
  devServer: {
    client: {
      overlay: false,
    },
  },
  webpack: {
    configure: (webpackConfig, { env, paths }) => {
      // Memory optimizations for production builds
      // (the DO app platform builder has limited RAM)
      if (env === 'production') {
        webpackConfig.optimization = {
          ...webpackConfig.optimization,
          splitChunks: {
            ...webpackConfig.optimization.splitChunks,
            maxSize: 244000, // Split large chunks to reduce memory pressure
          },
        };

        webpackConfig.performance = {
          ...webpackConfig.performance,
          maxAssetSize: 1000000, // 1MB limit to avoid processing huge assets
          maxEntrypointSize: 1000000,
        };
      }

      // Fix CRA #11770
      const rules = webpackConfig.module.rules;
      for (const rule of rules) {
        if (Object.hasOwn(rule, 'oneOf')) {
          rule.oneOf.filter((currentValue, index, arr) => {
            const toRemove =
              currentValue.test instanceof RegExp && currentValue.test.test('something.svg');
            if (toRemove) {
              arr.splice(index, 1);
            }
            return toRemove;
          });
          rule.oneOf.push({
            test: /\.svg$/i,
            issuer: {
              and: [/\.(ts|tsx|js|jsx|md|mdx)$/],
            },
            type: 'asset',
          });
        }
      }
      return webpackConfig;
    },
  },
};
