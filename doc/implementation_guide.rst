
Implementation Guide
====================

(this page is not finished yet)

This guide helps you implement and integrate poco-sdk with your game/app step by step.

Poco-sdk now supports following languages:

- python
- js
- lua
- c#
- java

More language will come in future.

Getting Poco SDK
----------------

First clone the `poco-sdk repo`_. Each languages are located in ``poco-sdk/sdk/*`` separately.

.. code-block:: bash

    git clone https://github.com/AirtestProject/Poco-SDK.git

You can just copy the source code of corresponding language to your project script folder.

Implement the Abstract Method
-----------------------------

xxx

Initialize poco-sdk after game launched
---------------------------------------

xxx


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


.. _poco-sdk repo: https://github.com/AirtestProject/Poco-SDK
