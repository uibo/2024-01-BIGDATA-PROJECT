const catchAsync = require('../utils/catchAsync');
const { joongoService } = require("../services");

const getJoongosInfoByYear = catchAsync(async (req, res) => {
    const data = { ...req.query, ...req.params, ...req.body };
    const result = await joongoService.getAveragePriceByYear(data);
    return res.send(result);
})

const getJoongosInfoByMonth = catchAsync(async (req, res) => {
    const data = { ...req.query, ...req.params, ...req.body };
    const result = await joongoService.getAveragePriceByMonth(data);
    return res.send(result);
})

const getJoongosInfoByDay = catchAsync(async (req, res) => {
    const data = { ...req.query, ...req.params, ...req.body };
    const result = await joongoService.getAveragePriceByDay(data);
    return res.send(result);
})

module.exports = {
    getJoongosInfoByYear,
    getJoongosInfoByMonth,
    getJoongosInfoByDay,
}
