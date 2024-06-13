const joi = require('joi');

const getJoongosInfoByYear = {
    query: joi.object().keys({
        model: joi.string(),
        battery: joi.number(),
        location: joi.string(),
        status: joi.number().valid(0, 1),
        featureList: joi.array().items(joi.string())
    }),
    params: joi.object().keys({}),
    body: joi.object().keys({}),
};
const getJoongosInfoByMonth = {
    query: joi.object().keys({
        model: joi.string(),
        battery: joi.number(),
        location: joi.string(),
        status: joi.number().valid(0, 1),
        featureList: joi.array().items(joi.string())
    }),
    params: joi.object().keys({}),
    body: joi.object().keys({}),
};
const getJoongosInfoByDay = {
    query: joi.object().keys({
        model: joi.string(),
        battery: joi.number(),
        location: joi.string(),
        status: joi.number().valid(0, 1),
        featureList: joi.array().items(joi.string())
    }),
    params: joi.object().keys({}),
    body: joi.object().keys({}),
};

module.exports = {
    getJoongosInfoByYear,
    getJoongosInfoByMonth,
    getJoongosInfoByDay,
};
