import React from "react";
import "./character.css"; // Assuming you have a CSS file for styling

const Characters = () => {
    const data =[
    {
        "name":"doctor",
        "img":"doctor.jpg"
    },
    {
        "name":"farmer",
        "img":"farmer.jpg"
    },
    {
        "name":"Cab Driver",
        "img":" cab driver.jpg"
    },
    {
        "name":"Tour Guide",
        "img":" tour guide.jpg"
    },
    {
        "name":"Engineer",
        "img":" engineer.jpg"
    },
    {
        "name":"Hotel manager",
        "img":" hotel manager.jpg"
    }
];
  return (
    <div className="container py-5">
      <section className="characters text-center">
        <h1 className="mb-5">Choose a Character to Chat</h1>
        <div className="row">
          {data && data.map((character, index) => (
            <div className="col-md-4 col-sm-6" key={index}>
              <div className="card h-100">
                <img
                  src={character.img}
                  className="card-img-top"
                  alt={`${character.name} image`}
                  style={{ height: "250px", objectFit: "cover" }}
                />
                <div className="card-body d-flex flex-column justify-content-between">
                  <h5 className="card-title">Chat with {character.name.charAt(0).toUpperCase() + character.name.slice(1)}</h5>
                  <p className="card-text">
                    Engage in a conversation with a {character.name} and explore their daily life.
                  </p>
                  <a href={`/chatp?character=${character.name}`} className="btn btn-primary mt-auto">
                    Chat
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default Characters;
