//-------RESTful API-------

//run this codes in your vs code terminal
/*
requirements: mongodb
              mongoose

--setup--
npm install express body-parser ejs mongoose express
npm i express body-parser ejs mongoose express

--run-
nodemon app.js
-------------*/



const express=require("express");
const bodyParser=require("body-parser");
const ejs=require("ejs");
const mongoose=require("mongoose");
const app=express();


app.set("view engine","ejs");

app.use(bodyParser.urlencoded({
extended:true
}));

app.use(express.static("public"));

mongoose.connect("mongodb://localhost:27017/cooksmart",{useNewUrlParser:true});

const recipeSchema={
    foodName:String,
    ingredients:String,
    Recipe:String
};

const RecipeAndIngredientGenerator=mongoose.model("recipeAndIngredientGenerator",recipeSchema);

//route handling (CHAINED ROUTING)
//both GET & POST using one single path
app.route("/home")
.get(function(req,res){
    RecipeAndIngredientGenerator.find(function(err,found){
        if(!err){
            res.send(found);
        }
        else{
            res.send(err);
        }
        
    });
})
.post(function(req,res){
    const newentry=new RecipeAndIngredientGenerator({
        foodName:req.body.foodName,
        ingredients:req.body.ingredients,
        Recipe:req.body.Recipe
    });
    newentry.save(function(err){
        if(!err){
            res.send("Successfully added the new data.");
        }
        else{
            res.send(err);
        }

    });
});


// GETTING THE RECIPE AND THE INGREDIENT FROM THE SPECIFIC FOOD ITEM
app.route("/home/:specificname")
.get(function(req,res){
    
    RecipeAndIngredientGenerator.findOne({foodName:req.params.specificname},function(err,found){
        if(found){
            res.send(found);
        }
        else{
            res.send("No  similar food name found in the document")
        }
    })

});



//---------------------------------SEPERATELY SHOWN HOW THE GET & POST METHOD WORKS-------------------------------------

//setting up the get route -> READ / GET
//the client gets the resources from the /home route


/* comment STARTS--

app.get("/home",function(req,res){
    RecipeAndIngredientGenerator.find(function(err,found){
        if(!err){
            res.send(found);
        }
        else{
            res.send(err);
        }
        
    });
});


-- COMMENT ENDS */
//get request can go to a specific resource 

/* comment STARTS--
app.get("/home/:specificname",function(req,res){
    
    RecipeAndIngredientGenerator.findOne({foodName:req.params.specificname},function(err,found){
        if(found){
            res.send(found);
        }
        else{
            res.send("No  similar food name found in the document")
        }
    })

});
       
-- COMMENT ENDS */


//setting up the post route -> POST 
//ASSUMPTION: - no front end, uses an api using postman
//post request should go to the collection of resources than the specific one

/* comment STARTS--

app.post("/home",function(req,res){
    

    //create a new  object  in the DB

    const newentry=new RecipeAndIngredientGenerator({
        //assumption : no front end
        //**find**
        //work with the list allergens buttons in the front end
        //sends data to the server via an api using postman
        foodName:req.body.foodName,
        ingredients:req.body.ingredients,
        Recipe:req.body.Recipe
    });
    //saving the new dataentry object to the DB
    newentry.save(function(err){
        if(!err){
            res.send("Successfully added the new data.");
        }
        else{
            res.send(err);
        }

    });
});


-- COMMENT ENDS */

//ADDITIONAL INFO IF NEEDED
//setting up the delete route -> DELETE

/*app.delete("/home",function(req,res){
    RecipeAndIngredientGenerator.deleteMany(function(err){
        if(!err){
            res.send("successfully deleted all the documents");
        }
        else{
            res.send(err);
        }
    });
})*/




app.listen(3000,function(){
    console.log("server started on port 3000")
})