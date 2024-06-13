var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var cors = require('cors');

const routes = require('./routes/v1');
const ApiError = require('./utils/ApiError');

var app = express();
app.use(cors({
        origin: '*',
}));

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/v1', routes);

// catch 404 and forward to error handler
app.use(function (req, res, next) {
  next(createError(404));
});

// error handler
// 임시 코드 사용
app.use(function (err, req, res, next) {
  const httpStatus = require('http-status');
  let error = err
  if (!(err instanceof ApiError)) {
    const statusCode =
      err?.statusCode || httpStatus.INTERNAL_SERVER_ERROR;
    const message = err?.message || httpStatus[statusCode];
    error = new ApiError(statusCode, message);
  }

  let { statusCode, message } = error;
  console.log(statusCode, message)
  res.locals.errorMessage = error.message;

  const response = {
    code: statusCode,
    message,
  };
  return res.status(statusCode).json(response);
});

module.exports = app;
