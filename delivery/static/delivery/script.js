document.addEventListener('DOMContentLoaded', () => {
    
    // Remove Skeleton Loader
    const skeletonLoader = document.getElementById('skeleton-loader');
    setTimeout(() => {
        skeletonLoader.classList.add('hide');
        setTimeout(() => {
            skeletonLoader.style.display = 'none';
        }, 500); // Wait for transition to finish
    }, 1500); // Simulate network load time

    // Sticky Navbar
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('sticky');
        } else {
            navbar.classList.remove('sticky');
        }
    });

    // Scroll Reveal Animation
    const reveals = document.querySelectorAll('.reveal');
    
    const revealOnScroll = () => {
        const windowHeight = window.innerHeight;
        const elementVisible = 100;

        reveals.forEach(reveal => {
            const elementTop = reveal.getBoundingClientRect().top;
            if (elementTop < windowHeight - elementVisible) {
                reveal.classList.add('active');
            }
        });
    };
    
    window.addEventListener('scroll', revealOnScroll);
    revealOnScroll(); // Trigger once on load

    // Active Navigation Link on Scroll
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-links a');

    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (pageYOffset >= (sectionTop - 200)) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').includes(current) && current !== '') {
                link.classList.add('active');
            }
        });
    });

    // Cart Sidebar Toggle
    const cartBtn = document.querySelector('.cart-btn');
    const closeCart = document.querySelector('.close-cart');
    const cartSidebar = document.querySelector('.cart-sidebar');
    const overlay = document.querySelector('.overlay');

    const toggleCart = () => {
        cartSidebar.classList.toggle('active');
        overlay.classList.toggle('active');
        document.body.classList.toggle('no-scroll');
    };

    cartBtn.addEventListener('click', toggleCart);
    closeCart.addEventListener('click', toggleCart);
    overlay.addEventListener('click', () => {
        if (cartSidebar.classList.contains('active')) {
            toggleCart();
        }
        if (document.querySelector('.nav-links').classList.contains('active')) {
            document.querySelector('.nav-links').classList.remove('active');
            overlay.classList.remove('active');
            document.body.classList.remove('no-scroll');
        }
    });

    // Mobile Menu Toggle
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navLinksContainer = document.querySelector('.nav-links');

    mobileToggle.addEventListener('click', () => {
        navLinksContainer.classList.toggle('active');
        overlay.classList.toggle('active');
        document.body.classList.toggle('no-scroll');
    });

    // Close mobile menu when a link is clicked
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navLinksContainer.classList.contains('active')) {
                navLinksContainer.classList.remove('active');
                overlay.classList.remove('active');
                document.body.classList.remove('no-scroll');
            }
        });
    });

    // Quantity Buttons in Cart (Basic interaction)
    const qtyButtons = document.querySelectorAll('.item-qty button');
    qtyButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const span = e.target.parentElement.querySelector('span');
            let currentQty = parseInt(span.innerText);
            
            if (e.target.innerText === '+') {
                span.innerText = currentQty + 1;
            } else if (e.target.innerText === '-' && currentQty > 1) {
                span.innerText = currentQty - 1;
            }
        });
    });

    // Add to Cart Button Animation (Simulated)
    const addButtons = document.querySelectorAll('.add-to-cart');
    const cartBadge = document.querySelector('.cart-badge');
    
    addButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            // Simple animation feedback
            const originalIcon = this.innerHTML;
            this.innerHTML = '<i class="fa-solid fa-check"></i>';
            this.style.backgroundColor = '#4caf50';
            this.style.color = '#fff';
            
            // Update cart count
            let count = parseInt(cartBadge.innerText);
            cartBadge.innerText = count + 1;
            
            // Pulse animation on badge
            cartBadge.style.transform = 'scale(1.5)';
            setTimeout(() => {
                cartBadge.style.transform = 'scale(1)';
            }, 300);

            setTimeout(() => {
                this.innerHTML = originalIcon;
                this.style.backgroundColor = '';
                this.style.color = '';
            }, 1000);
        });
    });

});
