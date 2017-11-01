
Implementation Guide
====================

This guide helps you implement and integrate poco-sdk with your game/app step by step.

Getting Poco SDK
----------------

First clone the poco repo according to your script language.

::

    # TODO: complete the git repo addr
    # for python
    git clone ssh://xxxx/poco.git


You can just copy the source code to your project or install it as 3rd party dependency.

Object Model
------------

This section shows key models and relationship between them.

Abstract Class/Interface Implementation
=======================================

To implement your own version of poco sdk, you only need to implement the following 2 classes/interfaces and override its abstract method. This section shows the details about implementing the abstract method in classes or interfaces.

:py:class:`AbstractNode <poco.sdk.AbstractNode>`
------------------------------------------------

4 methods should be override

:py:class:`AbstractNode <poco.sdk.AbstractDumper>`
--------------------------------------------------

1 method should be override
