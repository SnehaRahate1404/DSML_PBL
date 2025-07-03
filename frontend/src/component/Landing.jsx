import React from "react";
import { Link } from "react-router-dom";
import './Landing.css'; // Assuming you have a CSS file for styling

const Landing = () => {
  return (
    <>
   <body>
    
   
    <nav className="navbar ">
            <a className="navbar-brand" href="#">Proficiency Enhancer</a>
            {/* <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span className="navbar-toggler-icon"></span>
            </button> */}
            
                
            <a href="/accuracy" className="btn">Model Accuracy</a>
            

    </nav>

   
    <section className="hero-section">
        <div className="container">
            <div className="content">
                <h1>Boost Your English Proficiency</h1>
                <p>Start your personalized journey towards mastering English with interactive tools and intelligent assessments.</p>
                <a href="/characters" className="btn">Get Started</a>
            </div>
        </div>
    </section>

   
    <section className="card-section">
        <div className="container">
            <h2>Explore Your Learning Options</h2>
            <div className="container-part">
                <div className="col-md-4">
                    <div className="card">
                        <img src="practise.jpg" className="card-img-top" alt="Practice" />
                        <div className="card-body">
                            <h5 className="card-title">Interactive Practice</h5>
                            <p className="card-text">Engage in fun, interactive practice sessions to improve your English skills.</p>
                            <a href="/characters" className="btn-primary">Start Practicing</a>
                        </div>
                    </div>
                </div>
                <div className="col-md-4">
                    <div className="card">
                        <img src="assessment.png" className="card-img-top" alt="Assessment" />
                        <div className="card-body">
                            <h5 className="card-title">Personalized Assessments</h5>
                            <p className="card-text">Receive tailored feedback based on your progress and proficiency levels.</p>
                            <a href="/assessment" className="btn-primary">Take Assessment</a>
                        </div>
                    </div>
                </div>
                <div className="col-md-4">
                    <div className="card">
                        <img src="progress.jpg" className="card-img-top" alt="Track Progress" />
                        <div className="card-body">
                            <h5 className="card-title">Track Progress</h5>
                            <p className="card-text">Monitor your improvement over time and adjust your learning plans accordingly.</p>
                            <a href="/progress" className="btn-primary">Track Now</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

  
    
    </body>
    <footer>
        <p>&copy; 2024 Proficiency Enhancer. All Rights Reserved.</p>
    </footer>
</>
  );
};



export default Landing;
