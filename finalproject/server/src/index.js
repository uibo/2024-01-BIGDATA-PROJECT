const app = require('./app');
const config = require('./config/config');
const logger = require('morgan');
const {sequelize} = require('./models');
const {createSchema} = require("./config/mysql");

let server;

(async () => {
    try {
        // mysql 관련
        await createSchema();
        sequelize.sync({alter: true})
            .then(() => {
                // 서버 실행 관련
                server = app.listen(config.port, () => {
                    console.log('Listening to port %d', config.port);
                })
                server.keepAliveTimeout = 61 * 1000;
                server.headersTimeout = 65 * 1000; // This should be bigger than `keepAliveTimeout + your server's expected response time`
            })
            .catch((err) => {
                console.log(err);
            });
        
    } catch (e) {
        console.error(e);
        exitHandler();
    }
})()

const exitHandler = () => {
    if (server) {
        server.close(() => {
            console.log('Server closed');
            process.exit(1);
        })
    } else {
        process.exit(1);
    }
}

const unexpectedErrorHandler = (error) => {
    console.log(error)
    exitHandler();
}

process.on('uncaughtException', unexpectedErrorHandler);
process.on('unhandledRejection', unexpectedErrorHandler);

process.on('SIGINT', exitHandler);

