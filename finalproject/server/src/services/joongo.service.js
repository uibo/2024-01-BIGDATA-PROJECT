const { Joongo, sequelize } = require('../models/index')
const { Op } = require('sequelize');
const ApiError = require('../utils/ApiError');
const httpStatus = require('http-status');

const getAveragePriceByYear = async (data) => {
    try {
        const result = await Joongo.findAll({
            attributes: [
                'model',
                [sequelize.fn('DATE_FORMAT', sequelize.col('upload_date'), '%Y-01-01'), 'date'],
                [sequelize.fn('ROUND', sequelize.fn('AVG', sequelize.col('price'))), 'averagePrice'],
                [sequelize.fn('COUNT', sequelize.col('*')), 'count']
            ],
            group: ['model', sequelize.fn('DATE_FORMAT', sequelize.col('upload_date'), '%Y-01-01')],
            where: {
                ...(data.model && { model: data.model }),
                ...(data.location && {
                    location: { [Op.like]: `%${data.location}%` }
                }),
                ...(data.featureList && {
                    feature_list: {
                        [Op.and]: data.featureList.map(feature => ({
                            [Op.like]: `%${feature}%`
                        }))
                    }
                }),
                ...(data.battery !== null && data.battery !== undefined && {
                    battery: {
                        [Op.gte]: data.battery // battery가 battery 이상인 경우만 포함
                    }
                }),
                // input 으로 status가 들어온 경우만 처리 아니면 1(판매완료) 만 계산
                ...((data.status !== null && data.status !== undefined) ? {
                    status: data.status
                } : {
                    status: 1
                }
                ),
            },
            order: [['date', 'DESC']],
        });

        return result;
    } catch (error) {
        throw new ApiError(httpStatus.INTERNAL_SERVER_ERROR, error?.message ? `getAveragePriceByYear occured error : ${error?.message}` : "getAveragePriceByYear occured error");
    }
};

const getAveragePriceByMonth = async (data) => {
    try {
        const result = await Joongo.findAll({
            attributes: [
                'model',
                [sequelize.fn('DATE_FORMAT', sequelize.col('upload_date'), '%Y-%m-01'), 'date'],
                [sequelize.fn('ROUND', sequelize.fn('AVG', sequelize.col('price'))), 'averagePrice'],
                [sequelize.fn('COUNT', sequelize.col('*')), 'count']
            ],
            group: ['model', sequelize.fn('DATE_FORMAT', sequelize.col('upload_date'), '%Y-%m-01')],
            where: {
                ...(data.model && { model: data.model }),
                ...(data.location && {
                    location: { [Op.like]: `%${data.location}%` }
                }),
                ...(data.featureList && {
                    feature_list: {
                        [Op.and]: data.featureList.map(feature => ({
                            [Op.like]: `%${feature}%`
                        }))
                    }
                }),
                ...(data.battery !== null && data.battery !== undefined && {
                    battery: {
                        [Op.gte]: data.battery // battery가 battery 이상인 경우만 포함
                    }
                }),
                // input 으로 status가 들어온 경우만 처리 아니면 1(판매완료) 만 계산
                ...((data.status !== null && data.status !== undefined) ? {
                    status: data.status
                } : {
                    status: 1
                }
                ),
            },
            order: [['date', 'DESC']],
        });

        return result;
    } catch (error) {
        throw new ApiError(httpStatus.INTERNAL_SERVER_ERROR, error?.message ? `getAveragePriceByMonth occured error : ${error?.message}` : "getAveragePriceByMonth occured error");
    }
};

const getAveragePriceByDay = async (data) => {
    try {
        const result = await Joongo.findAll({
            attributes: [
                'model',
                [sequelize.fn('DATE_FORMAT', sequelize.col('upload_date'), '%Y-%m-%d'), 'date'],
                [sequelize.fn('ROUND', sequelize.fn('AVG', sequelize.col('price'))), 'averagePrice'],
                [sequelize.fn('COUNT', sequelize.col('*')), 'count']
            ],
            group: ['model', sequelize.fn('DATE_FORMAT', sequelize.col('upload_date'), '%Y-%m-%d')],
            where: {
                ...(data.model && { model: data.model }),
                ...(data.location && {
                    location: { [Op.like]: `%${data.location}%` }
                }),
                ...(data.featureList && {
                    feature_list: {
                        [Op.and]: data.featureList.map(feature => ({
                            [Op.like]: `%${feature}%`
                        }))
                    }
                }),
                ...(data.battery !== null && data.battery !== undefined && {
                    battery: {
                        [Op.gte]: data.battery // battery가 battery 이상인 경우만 포함
                    }
                }),
                // input 으로 status가 들어온 경우만 처리 아니면 1(판매완료) 만 계산
                ...((data.status !== null && data.status !== undefined) ? {
                    status: data.status
                } : {
                    status: 1
                }
                ),
            },
            order: [['date', "DESC"]]
        });

        return result;
    } catch (error) {
        throw new ApiError(httpStatus.INTERNAL_SERVER_ERROR, error?.message ? `getAveragePriceByDay occured error : ${error?.message}` : "getAveragePriceByDay occured error");
    }
};


module.exports = {
    getAveragePriceByYear,
    getAveragePriceByMonth,
    getAveragePriceByDay,
}
