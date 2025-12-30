import dash_bootstrap_components as dbc
from dash import html

def create_navibar():
    return dbc.Navbar(
        dbc.Container(
            [
                # Brand Title
                dbc.NavbarBrand(
                    "Rocket Launch Analytics", 
                    className="ms-2 fw-bold", 
                    style={"color": "#007bff", "fontSize": "1.5rem"},
                    href="/"
                ),
                
                # Navbar Toggler for small screens
                dbc.NavbarToggler(id="navbar-toggler"),
                
                # Collapsible Navigation Links
                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavItem(dbc.NavLink("EDA", href="/", className="nav-link", style={"color": "#343a40"})),
                            dbc.NavItem(dbc.NavLink("Webscraping", href="/scraping", className="nav-link", style={"color": "#343a40"})),
                            dbc.NavItem(dbc.NavLink("Interactive Map", href="/folium", className="nav-link", style={"color": "#343a40"})),
                            dbc.NavItem(dbc.NavLink("About", href="#", className="nav-link", id="about-link", style={"color": "#343a40"})),
                            # Dropdown Menu Example
                            dbc.DropdownMenu(
                                label="More",
                                children=[
                                    dbc.DropdownMenuItem(
                                        html.Span([
                                            html.I(className="fab fa-linkedin me-2"),
                                            "LinkedIn"
                                        ]),
                                        href="https://www.linkedin.com/in/helena-software-engineer/",
                                        target="_blank"
                                    ),
                                    dbc.DropdownMenuItem(
                                        html.Span([
                                            html.I(className="fas fa-briefcase me-2"),
                                            "Portfolio"
                                        ]),
                                        href="https://myportfolio.hmpedro.com/",
                                        target="_blank"
                                    ),
                                ],
                                nav=True,
                                in_navbar=True,
                                className="text-dark",
                            ),
                        ],
                        className="ms-auto",
                        navbar=True,
                    ),
                    id="navbar-collapse",
                    navbar=True,
                ),
            ],
            fluid=True,
        ),
        color="light", 
        dark=False,      
        sticky="top",    # Navbar stays at the top
        className="shadow-sm",
    )
