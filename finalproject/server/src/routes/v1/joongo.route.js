const express = require('express');
const { joongoController } = require('../../controllers');
const validate = require('../../middlewares/validate');
const { joongoValidation } = require('../../validation');
const router = express.Router();

router
    .route('/year')
    .get(validate(joongoValidation.getJoongosInfoByYear), joongoController.getJoongosInfoByYear)
router
    .route('/month')
    .get(validate(joongoValidation.getJoongosInfoByMonth), joongoController.getJoongosInfoByMonth)
router
    .route('/day')
    .get(validate(joongoValidation.getJoongosInfoByDay), joongoController.getJoongosInfoByDay)

module.exports = router;
