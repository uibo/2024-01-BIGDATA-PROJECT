const Sequelize = require('sequelize');
const config = require('../config/config');

let sequelize;

sequelize = new Sequelize(config.sequelize.database, config.sequelize.username, config.sequelize.password, {
    host: config.sequelize.host,
    port: config.sequelize.port,
    dialect: config.sequelize.dialect,
    timezone: '+09:00',
    pool: {
        max: 20,
        min: 0,
    },
    logging: false,
    define: {
        timestamps: false, 
        createdAt: 'created_at',
        updatedAt: 'updated_at',
        deletedAt: 'deleted_at',
    }
});

const Joongo = require('./joongo.model')(sequelize, Sequelize);
// Joongo.removeAttribute('id');
module.exports = {
    sequelize,
    Joongo
}
