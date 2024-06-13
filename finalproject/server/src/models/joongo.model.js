module.exports = (sequelize, DataTypes) => {
    const schema = {
        id: {
            type: DataTypes.INTEGER,
            primaryKey: true,
            autoIncrement: true,
        },
        model: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        feature_list: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        battery: {
            type: DataTypes.INTEGER,
            allowNull: false,
        },
        upload_date: {
            type: DataTypes.DATE,
            allowNull: false,
        },
        price: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        status: {
            type: DataTypes.TINYINT,
            allowNull: false,
        },
        location: {
            type: DataTypes.TEXT,
            allowNull: false,
        },
        imgUrl: {
            type: DataTypes.TEXT,
            allowNull: false,
        },
        url: {
            type: DataTypes.TEXT,
            allowNull: false,
        },
    };

    const modelOptions = {
        tableName: 'joongo',
        indexes: [],
        timestamps: false,
    };

    return sequelize.define('Joongo', schema, modelOptions);
};
