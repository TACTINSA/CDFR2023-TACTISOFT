const svgSprite = require("eleventy-plugin-svg-sprite");
const eleventyNavigationPlugin = require("@11ty/eleventy-navigation");

module.exports = function (eleventyConfig) {
    eleventyConfig.addPassthroughCopy({"src/static_assets/assets": "assets"});
    eleventyConfig.addPlugin(svgSprite, {
        path: "./src/static_assets/assets/svg"
    });
    eleventyConfig.addPlugin(eleventyNavigationPlugin);

    return {
        dir: {
            input: "src", output: "public"
        },
    };
};