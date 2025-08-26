Contributing Guide
==================

We welcome contributions to the Image AI Detector project! This guide will help you get started.

Ways to Contribute
------------------

🐛 **Report Bugs**
   Found an issue? Open a GitHub issue with details.

💡 **Suggest Features**
   Have ideas for improvements? We'd love to hear them.

📝 **Improve Documentation**
   Help make our docs clearer and more comprehensive.

🔧 **Submit Code**
   Fix bugs, add features, or optimize performance.

🧪 **Test & Review**
   Try new features and provide feedback.

Getting Started
---------------

Development Setup
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # 1. Fork the repository on GitHub
   # 2. Clone your fork
   git clone https://github.com/YOUR_USERNAME/image-ai-detector.git
   cd image-ai-detector

   # 3. Set up development environment
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements-ml.txt  # Includes dev dependencies

   # 4. Install pre-commit hooks
   pre-commit install

   # 5. Create a feature branch
   git checkout -b feature/your-feature-name

Code Style
~~~~~~~~~~

We use standard Python and JavaScript formatting:

.. tabs::

   .. tab:: Python

      .. code-block:: bash

         # Format with black
         black *.py

         # Lint with flake8
         flake8 *.py

         # Type check with mypy
         mypy simple_ai_detector.py

   .. tab:: JavaScript

      .. code-block:: bash

         # Format with prettier
         npx prettier --write *.js

         # Lint with eslint
         npx eslint *.js

   .. tab:: Pre-commit

      .. code-block:: bash

         # Run all checks
         pre-commit run --all-files

Project Structure
-----------------

.. code-block:: text

   image-ai-detector/
   ├── manifest.json              # Chrome extension manifest
   ├── background.js              # Extension background script
   ├── content-script.js          # Page injection script
   ├── popup.html/js              # Extension UI
   ├── options.html/js            # Settings page
   ├── simple_ai_detector.py      # Main API server
   ├── ml_model_example.py        # Example ML implementation
   ├── requirements.txt           # Production dependencies
   ├── requirements-ml.txt        # Development dependencies
   ├── tests/                     # Test suite
   ├── docs/                      # Original markdown docs
   └── sphinx-docs/               # Sphinx documentation

Types of Contributions
----------------------

Bug Fixes
~~~~~~~~~~

1. **Identify the Issue**
   - Check existing issues first
   - Reproduce the bug locally
   - Understand the root cause

2. **Create a Fix**
   - Write minimal code changes
   - Add tests if applicable
   - Update documentation

3. **Submit Pull Request**
   - Clear description of the problem
   - Explanation of the solution
   - Link to related issues

Feature Development
~~~~~~~~~~~~~~~~~~~

1. **Discuss First**
   - Open an issue to discuss the feature
   - Get feedback from maintainers
   - Ensure it aligns with project goals

2. **Implementation**
   - Follow existing code patterns
   - Add comprehensive tests
   - Update documentation

3. **Testing**
   - Test across different browsers
   - Verify API compatibility
   - Check performance impact

Documentation
~~~~~~~~~~~~~

We use Sphinx for documentation:

.. code-block:: bash

   # Install docs dependencies
   pip install sphinx furo myst-parser

   # Build documentation
   cd sphinx-docs
   make html

   # View locally
   open _build/html/index.html

Testing Guidelines
------------------

Running Tests
~~~~~~~~~~~~~

.. code-block:: bash

   # Run all tests
   python -m pytest tests/

   # Run with coverage
   python -m pytest tests/ --cov=. --cov-report=html

   # Run specific test
   python -m pytest tests/test_api.py::test_classify_endpoint

Writing Tests
~~~~~~~~~~~~~

.. tabs::

   .. tab:: API Tests

      .. code-block:: python

         import pytest
         from simple_ai_detector import app

         @pytest.fixture
         def client():
             app.config['TESTING'] = True
             with app.test_client() as client:
                 yield client

         def test_health_endpoint(client):
             response = client.get('/health')
             assert response.status_code == 200
             data = response.get_json()
             assert data['status'] == 'healthy'

   .. tab:: Extension Tests

      .. code-block:: javascript

         // tests/extension.test.js
         describe('Image Detection', () => {
           test('finds visible images', () => {
             // Mock DOM with images
             document.body.innerHTML = `
               <img src="test.jpg" width="100" height="100">
             `;
             
             const images = findVisibleImages();
             expect(images).toHaveLength(1);
           });
         });

   .. tab:: Integration Tests

      .. code-block:: python

         def test_end_to_end_classification():
             # Start server
             # Load extension
             # Trigger analysis
             # Verify results
             pass

Pull Request Process
--------------------

1. **Before Submitting**

   .. code-block:: bash

      # Ensure tests pass
      python -m pytest tests/
      
      # Run linting
      pre-commit run --all-files
      
      # Update documentation if needed
      cd sphinx-docs && make html

2. **PR Template**

   .. code-block:: markdown

      ## Description
      Brief description of changes

      ## Type of Change
      - [ ] Bug fix
      - [ ] New feature
      - [ ] Documentation update
      - [ ] Performance improvement

      ## Testing
      - [ ] Tests pass locally
      - [ ] Added new tests for new functionality
      - [ ] Manual testing completed

      ## Screenshots (if applicable)

3. **Review Process**
   - Automated checks must pass
   - At least one maintainer review
   - Address feedback promptly
   - Squash commits before merge

Development Areas
-----------------

High Priority
~~~~~~~~~~~~~

🎯 **Performance Optimization**
   - Reduce API latency
   - Improve caching strategies
   - Optimize image preprocessing

🧠 **ML Model Improvements**
   - Experiment with different models
   - Implement ensemble methods
   - Add confidence calibration

🔧 **Extension Features**
   - Batch image analysis
   - Custom confidence thresholds
   - Results export functionality

Medium Priority
~~~~~~~~~~~~~~~

📱 **Cross-Platform Support**
   - Firefox extension port
   - Safari extension support
   - Mobile browser compatibility

🎨 **UI/UX Enhancements**
   - Improved badge styling
   - Animation effects
   - Accessibility improvements

🔒 **Security & Privacy**
   - Local model inference
   - Enhanced privacy controls
   - Security audit

Research Areas
~~~~~~~~~~~~~~

🧪 **Experimental Features**
   - Attention visualization
   - Adversarial robustness
   - Multi-modal analysis

📊 **Analytics & Metrics**
   - Performance monitoring
   - Usage analytics
   - Error tracking

🌐 **Deployment Options**
   - Cloud deployment guides
   - Docker containers
   - Serverless functions

Code Review Checklist
----------------------

For Reviewers
~~~~~~~~~~~~~

✅ **Functionality**
- [ ] Code works as intended
- [ ] Edge cases handled
- [ ] Error handling appropriate
- [ ] Performance acceptable

✅ **Code Quality**
- [ ] Follows project conventions
- [ ] Well-documented
- [ ] No code duplication
- [ ] Appropriate abstractions

✅ **Testing**
- [ ] Tests cover new functionality
- [ ] Tests are meaningful
- [ ] All tests pass
- [ ] Coverage maintained

For Contributors
~~~~~~~~~~~~~~~~

✅ **Before Submitting**
- [ ] Tests pass locally
- [ ] Linting passes
- [ ] Documentation updated
- [ ] Commit messages clear

✅ **PR Description**
- [ ] Clear problem statement
- [ ] Solution explanation
- [ ] Testing approach
- [ ] Breaking changes noted

Community Guidelines
--------------------

Code of Conduct
~~~~~~~~~~~~~~~

- **Be Respectful**: Treat everyone with kindness and respect
- **Be Inclusive**: Welcome contributors from all backgrounds
- **Be Constructive**: Provide helpful feedback and suggestions
- **Be Patient**: Remember that everyone is learning

Communication
~~~~~~~~~~~~~

- **GitHub Issues**: Bug reports and feature requests
- **Pull Requests**: Code contributions and discussions
- **Discussions**: General questions and ideas

Recognition
~~~~~~~~~~~

Contributors are recognized in:
- README.md contributors section
- Release notes for significant contributions
- Special thanks in documentation

Getting Help
------------

Stuck on something? Here's how to get help:

1. **Documentation**: Check existing docs first
2. **Search Issues**: Look for similar problems
3. **Ask Questions**: Open a discussion or issue
4. **Join Community**: Connect with other contributors

**Maintainer Contact:**
- GitHub: `@rithwikgokhale <https://github.com/rithwikgokhale>`_
- Issues: `Project Issues <https://github.com/rithwikgokhale/image-ai-detector/issues>`_

Thank you for contributing to Image AI Detector! 🚀
