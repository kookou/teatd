import React from 'react';
import PropTypes from 'prop-types';
import { makeStyles, useTheme } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Rating from '@material-ui/lab/Rating';



const useStyles = makeStyles((theme) => ({
    divroot: {
        flexGrow: 1,
        marginBottom: theme.spacing(2),
        width: "100%",
    },
    root: {
        // display: 'flex',
        width: 290,
    },
    details: {
        display: 'flex',
        flexDirection: 'column',
    },
    cover: {
        width: 150,
        height: 150,
    },
    paper: {
        // padding: theme.spacing(2),
        textAlign: 'center',
        color: theme.palette.text.secondary,
    },
    media: {
        height: 140,
    },
    mrr: {
        marginRight: theme.spacing(1)
    },
    mrb: {
        marginTop: theme.spacing(2),
    },
    rating:{
        marginTop : 2,
    }
}));


function HalfRating() {
    const classes = useStyles();
    const [value, setValue] = React.useState(4);
    return (
        <div className={classes.root}>
            <Rating name="read-only" value={value} readOnly />
        </div>
    );
}

const ChatbotMenuSearchContents = (props) => {
    // console.log("뭐올거니"+JSON.stringify(props))
    // console.log("아악"+props)
    const classes = useStyles();
    const theme = useTheme();
    const post  = props.menu[0];
    // console.log("post "+props.menu[0].food_img)
    const userid = sessionStorage.getItem("sessionUser");
    return (

        <div className={classes.divroot}>
            <Grid container justify="flex-start" >
                <Grid>
                    <Card className={classes.root} square elevation={0} variant="outlined" >
                        <CardActionArea >
                            <CardMedia
                                className={classes.media}
                                image={'https://www.yogiyo.co.kr' + post.shop_img}
                                title="Contemplative Reptile"
                            />
                            <CardContent>
                                <Typography variant="body2" >
                                    {post.shop_name}
                                </Typography>
                                <Typography variant="body2" >
                                    {post.price}원
                                </Typography>
                                <Grid container direction="row">
                                    {/* <Typography gutterBottom variant="caption" color="textSecondary" className={classes.mrr}>
                                        {post.shop_name}
                                    </Typography> */}
                                    <Rating name="iconstar" defaultValue={1} max={1} size="small" className={classes.rating}/>
                                    <Typography variant="caption" color="textSecondary">
                                        {post.shop_rev_avg}
                                    </Typography>
                                </Grid>
                            </CardContent>
                        </CardActionArea>
                    </Card>
                    <Grid container justify="center" className={classes.mrb}>
                        <Typography variant="subtitle2" >
                            {userid}님의 예상 평점 {post.shop_pred_avg}
                        </Typography>
                    </Grid>
                </Grid>

            </Grid>
        </div >


    );
}

ChatbotMenuSearchContents.propTypes = {
    post: PropTypes.object,
};

export default ChatbotMenuSearchContents