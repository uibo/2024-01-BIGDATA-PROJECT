const dotenv = require('dotenv');
const path = require('path');
const joi = require('joi');

dotenv.config({path: path.join(__dirname, '../../.env')});

const envVarSchema = joi.object()
    .keys({
        NODE_ENV: joi.string().valid('production', 'development', 'test').required(),
        PORT: joi.number().default(20246),
        
        // sql 관련
        SQL_HOST: joi.string().required(),
        SQL_PORT: joi.number().required(),
        SQL_DATABASE: joi.string().required(),
        SQL_USERNAME: joi.string().required(),
        SQL_PASSWORD: joi.string().required(),
        SQL_DIALECT: joi.string().required().valid('mysql', 'postgres', 'mssql'),
    })
    .unknown();

const {value: envVars, error} = envVarSchema.prefs({errors: {label: 'key'}}).validate(process.env);

if (error) {
    throw new Error(`Config validation error: ${error.message}`);
}

module.exports = {
    env: envVars.NODE_ENV,
    port: envVars.PORT,
    
    // sql 관련
    sequelize: {
        database: envVars.SQL_DATABASE,
        username: envVars.SQL_USERNAME,
        password: envVars.SQL_PASSWORD,
        host: envVars.SQL_HOST,
        port: envVars.SQL_PORT,
        dialect: envVars.SQL_DIALECT,
    },
    
};
