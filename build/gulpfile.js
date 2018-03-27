var gulp = require('gulp');
var debug = require('gulp-debug');
var path = require('path');
var plugins = require('gulp-load-plugins')();
var flatten = require('gulp-flatten');
var sourcemaps = require('gulp-sourcemaps');

// Plugins
var sass = require('gulp-sass');
var minifyCss = require('gulp-minify-css');

var buildEnv = plugins.util.env.environment || 'development';
var config = require('./config/'+buildEnv+'.json');

// Shared error handler
function handleError(err) {
    console.log(err.toString());
    this.emit('end');
}

gulp.task('sass-build', function() {
    return gulp
        .src([
            path.join(config.src, '**/scss/**/[^_]*.scss')
        ])
        .pipe(debug())
        .pipe(sourcemaps.init())
        .pipe(sass().on('error', sass.logError)).on('error', handleError)
        .pipe(config.minify ? minifyCss() : plugins.util.noop())
        .pipe(flatten())
        .pipe(sourcemaps.write('./'))
        .pipe(gulp.dest(path.join(config.dest, 'css')));
});

gulp.task('build', ['sass-build'], function() {

});

gulp.task('watch', ['build'], function() {
    gulp.watch(path.join(config.src, '**/scss/**/*.scss'), ['sass-build']);
});

gulp.task('default', ['build']);
