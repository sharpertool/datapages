import gulp from 'gulp';
import debug from 'gulp-debug';
import {join} from 'path';
import noop from 'gulp-noop';

import flatten from 'gulp-flatten';
import sourcemaps from 'gulp-sourcemaps';
import sass from 'gulp-sass';
import cleanCSS from 'gulp-clean-css';
import gulpLoadPlugins from 'gulp-load-plugins';

let plugins = gulpLoadPlugins();

//console.log(`Environment: ${JSON.stringify(plugins.util.env)}`)
let buildEnv = process.env.environment || 'development';
//let buildEnv = 'development'
let config = require('./config/' + buildEnv + '.json');
console.log(`Config environment name ${config.name}`);

// Shared error handler
function handleError(err) {
    console.log(err.toString());
    this.emit('end');
}

gulp.task('sass-build', function() {
    return gulp
        .src([
            join(config.src, '**/scss/**/[^_]*.scss')
        ])
        .pipe(debug())
        .pipe(config.srcmap ? sourcemaps.init() : noop())
        .pipe(sass().on('error', sass.logError)).on('error', handleError)
        .pipe(flatten())
        .pipe(config.srcmap ? sourcemaps.write('./') : noop())
        .pipe(config.minify ? cleanCSS() : noop())
        .pipe(gulp.dest(join(config.dest, 'css')));
});

gulp.task('build', ['sass-build'], function() {

});

gulp.task('watch', ['build'], function() {
    gulp.watch(join(config.src, '**/scss/**/*.scss'), ['sass-build']);
});

gulp.task('default', ['build']);
