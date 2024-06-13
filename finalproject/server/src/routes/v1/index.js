const express = require('express');
const joongoRoute = require('./joongo.route');

const router = express.Router();

const defaultRoutes = [
    {
        path : '/joongos',
        route: joongoRoute,
    },
];

defaultRoutes.forEach((route) => {
    router.use(route.path, route.route)
})

module.exports = router;
