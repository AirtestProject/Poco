

<!DOCTYPE html>
<!--[if IE 8]><html class="no-js lt-ie9" lang="en" > <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en" > <!--<![endif]-->
<head>
  <meta charset="utf-8">
  
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
  <title>Poco ポコ &mdash; poco  documentation</title>
  

  
  
  
  

  

  
  
    

  

  
  
    <link rel="stylesheet" href="../_static/css/theme.css" type="text/css" />
  

  

  
        <link rel="index" title="Index"
              href="../genindex.html"/>
        <link rel="search" title="Search" href="../search.html"/>
    <link rel="top" title="poco  documentation" href="../index.html"/>
        <link rel="next" title="poco package" href="poco.html"/>
        <link rel="prev" title="Welcome to Poco’s documentation!" href="../index.html"/> 

  
  <script src="../_static/js/modernizr.min.js"></script>

</head>

<body class="wy-body-for-nav" role="document">

   
  <div class="wy-grid-for-nav">

    
    <nav data-toggle="wy-nav-shift" class="wy-nav-side">
      <div class="wy-side-scroll">
        <div class="wy-side-nav-search">
          

          
            <a href="../index.html" class="icon icon-home"> poco
          

          
          </a>

          
            
            
          

          
<div role="search">
  <form id="rtd-search-form" class="wy-form" action="../search.html" method="get">
    <input type="text" name="q" placeholder="Search docs" />
    <input type="hidden" name="check_keywords" value="yes" />
    <input type="hidden" name="area" value="default" />
  </form>
</div>

          
        </div>

        <div class="wy-menu wy-menu-vertical" data-spy="affix" role="navigation" aria-label="main navigation">
          
            
            
              
            
            
              <ul class="current">
<li class="toctree-l1 current"><a class="current reference internal" href="#">Poco ポコ</a><ul>
<li class="toctree-l2"><a class="reference internal" href="#features">Features</a></li>
<li class="toctree-l2"><a class="reference internal" href="#installation">Installation</a></li>
<li class="toctree-l2"><a class="reference internal" href="#example">Example</a></li>
<li class="toctree-l2"><a class="reference internal" href="#basic-concepts">Basic Concepts</a><ul>
<li class="toctree-l3"><a class="reference internal" href="#definitions-of-coordinate-system-and-metric-space">Definitions of coordinate system and metric space</a><ul>
<li class="toctree-l4"><a class="reference internal" href="#normalized-coordinate-system">Normalized Coordinate System</a></li>
<li class="toctree-l4"><a class="reference internal" href="#local-coordinate-system-local-positioning">Local Coordinate System (local positioning)</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="#poco-instance">Poco Instance</a></li>
<li class="toctree-l2"><a class="reference internal" href="#object-selection-and-operation">Object Selection and Operation</a><ul>
<li class="toctree-l3"><a class="reference internal" href="#basic-selector">Basic Selector</a></li>
<li class="toctree-l3"><a class="reference internal" href="#relative-selector">Relative Selector</a></li>
<li class="toctree-l3"><a class="reference internal" href="#sequence-selector-index-selector-iterator-is-more-recommended-for-use">Sequence Selector (index selector, iterator is more recommended for use)</a></li>
<li class="toctree-l3"><a class="reference internal" href="#iterate-over-a-collection-of-objects">Iterate over a collection of objects</a></li>
<li class="toctree-l3"><a class="reference internal" href="#get-object-properties">Get object properties</a></li>
<li class="toctree-l3"><a class="reference internal" href="#object-proxy-related-operation">Object Proxy Related Operation</a><ul>
<li class="toctree-l4"><a class="reference internal" href="#click">click</a></li>
<li class="toctree-l4"><a class="reference internal" href="#swipe">swipe</a></li>
<li class="toctree-l4"><a class="reference internal" href="#drag">drag</a></li>
<li class="toctree-l4"><a class="reference internal" href="#focus-local-positioning">focus (local positioning)</a></li>
<li class="toctree-l4"><a class="reference internal" href="#wait">wait</a></li>
</ul>
</li>
<li class="toctree-l3"><a class="reference internal" href="#global-operation">Global Operation</a><ul>
<li class="toctree-l4"><a class="reference internal" href="#click">click</a></li>
<li class="toctree-l4"><a class="reference internal" href="#swipe">swipe</a></li>
<li class="toctree-l4"><a class="reference internal" href="#snapshot">snapshot</a></li>
</ul>
</li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="#exceptions">Exceptions</a><ul>
<li class="toctree-l3"><a class="reference internal" href="#pocotargettimeout">PocoTargetTimeout</a></li>
<li class="toctree-l3"><a class="reference internal" href="#poconosuchnodeexception">PocoNoSuchNodeException</a></li>
</ul>
</li>
<li class="toctree-l2"><a class="reference internal" href="#unit-test">Unit Test</a></li>
</ul>
</li>
</ul>
<ul>
<li class="toctree-l1"><a class="reference internal" href="poco.html">poco package</a></li>
<li class="toctree-l1"><a class="reference internal" href="poco.proxy.html">poco.proxy module</a></li>
<li class="toctree-l1"><a class="reference internal" href="poco.exceptions.html">poco.exceptions module</a></li>
<li class="toctree-l1"><a class="reference internal" href="poco.sdk.html">poco.sdk package</a></li>
</ul>

            
          
        </div>
      </div>
    </nav>

    <section data-toggle="wy-nav-shift" class="wy-nav-content-wrap">

      
      <nav class="wy-nav-top" role="navigation" aria-label="top navigation">
        
          <i data-toggle="wy-nav-top" class="fa fa-bars"></i>
          <a href="../index.html">poco</a>
        
      </nav>


      
      <div class="wy-nav-content">
        <div class="rst-content">
          















<div role="navigation" aria-label="breadcrumbs navigation">

  <ul class="wy-breadcrumbs">
    
      <li><a href="../index.html">Docs</a> &raquo;</li>
        
      <li>Poco ポコ</li>
    
    
      <li class="wy-breadcrumbs-aside">
        
            
            <a href="../_sources/source/README.md.txt" rel="nofollow"> View page source</a>
          
        
      </li>
    
  </ul>

  
  <hr/>
</div>
          <div role="main" class="document" itemscope="itemscope" itemtype="http://schema.org/Article">
           <div itemprop="articleBody">
            
  <div class="section" id="poco">
<span id="poco"></span><h1>Poco ポコ<a class="headerlink" href="#poco" title="Permalink to this headline">¶</a></h1>
<p><strong>A cross-engine UI automation framework</strong></p>
<p><a class="reference external" href="README-CN.md">中文README(Chinese README)</a>在此。</p>
<div class="section" id="features">
<span id="features"></span><h2>Features<a class="headerlink" href="#features" title="Permalink to this headline">¶</a></h2>
<ul class="simple">
<li>Support mainstream game engines, including: Unity3D, cocos2dx-js, cocos2dx-lua and Android native apps.</li>
<li>Retrieve UI Elements Hierarchy in game's runtime.</li>
<li>Super fast and impact-free to the game.</li>
<li>Super easy sdk integration to the game in 5 minutes.</li>
<li>Powerful APIs which are engine independent.</li>
<li>Support multi-touch e.g. fling/pinch/etc. (in development)</li>
<li>Support gps, gyros, rotation (landscape/portrait) and other sensors as input.  (in development)</li>
<li>Extensible to other private engines by implementing <a class="reference external" href="#">poco-sdk</a>.</li>
<li>Compatible with Python 2.7 and Python 3.3+.</li>
</ul>
</div>
<div class="section" id="installation">
<span id="installation"></span><h2>Installation<a class="headerlink" href="#installation" title="Permalink to this headline">¶</a></h2>
<p>To use poco, you should install poco on your host as a python library and integrate <a class="reference external" href="source/doc/integration.html">poco-sdk</a> in your game.</p>
<p><strong>poco</strong> can be installed with pip:</p>
<div class="highlight-default"><div class="highlight"><pre><span></span><span class="c1"># In the future</span>
<span class="n">pip</span> <span class="n">install</span> <span class="n">poco</span>
</pre></div>
</div>
<div class="highlight-default"><div class="highlight"><pre><span></span><span class="c1"># Currently, it is only available in git repo. So please clone the repo and install</span>
<span class="n">git</span> <span class="n">clone</span> <span class="n">xxx</span><span class="o">/</span><span class="n">poco</span><span class="o">.</span><span class="n">git</span>
<span class="n">pip</span> <span class="n">install</span> <span class="o">-</span><span class="n">e</span> <span class="n">poco</span>
</pre></div>
</div>
<p><strong>poco-sdk</strong> integration please refer to <a class="reference external" href="source/doc/integration.html">Integration Guide</a>.</p>
</div>
<div class="section" id="example">
<span id="example"></span><h2>Example<a class="headerlink" href="#example" title="Permalink to this headline">¶</a></h2>
<p>The following example shows a simple test script on demo game using Unity3D. More examples <a class="reference external" href="#">here</a>.</p>
<div class="highlight-python"><div class="highlight"><pre><span></span><span class="kn">from</span> <span class="nn">poco.drivers.unity3d</span> <span class="kn">import</span> <span class="n">UnityPoco</span> <span class="k">as</span> <span class="n">Poco</span>

<span class="n">poco</span> <span class="o">=</span> <span class="n">Poco</span><span class="p">((</span><span class="s1">&#39;localhost&#39;</span><span class="p">,</span> <span class="mi">5001</span><span class="p">))</span>

<span class="c1"># tap start button</span>
<span class="n">poco</span><span class="p">(</span><span class="s1">&#39;start_btn&#39;</span><span class="p">,</span> <span class="nb">type</span><span class="o">=</span><span class="s1">&#39;Button&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">click</span><span class="p">()</span>

<span class="c1"># collect all &#39;stars&#39; to my &#39;bag&#39; by dragging the star icon</span>
<span class="n">bag</span> <span class="o">=</span> <span class="n">poco</span><span class="p">(</span><span class="s1">&#39;bag_area&#39;</span><span class="p">)</span>
<span class="k">for</span> <span class="n">star</span> <span class="ow">in</span> <span class="n">poco</span><span class="p">(</span><span class="nb">type</span><span class="o">=</span><span class="s1">&#39;MPanel&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">child</span><span class="p">(</span><span class="s1">&#39;star&#39;</span><span class="p">):</span>
    <span class="n">star</span><span class="o">.</span><span class="n">drag_to</span><span class="p">(</span><span class="n">bag</span><span class="p">)</span>

<span class="c1"># click Text starting with &#39;finish&#39; to finish collecting</span>
<span class="n">poco</span><span class="p">(</span><span class="n">textMatches</span><span class="o">=</span><span class="s1">&#39;finish.*&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">click</span><span class="p">()</span>
</pre></div>
</div>
</div>
<div class="section" id="basic-concepts">
<span id="basic-concepts"></span><h2>Basic Concepts<a class="headerlink" href="#basic-concepts" title="Permalink to this headline">¶</a></h2>
<ul class="simple">
<li><strong>Target device</strong>: test devices apps or games will run on, usually refers to mobile phones</li>
<li><strong>UI proxy</strong>: proxy objects within poco framework, representing 0, 1 or multiple in-game UI elements</li>
<li><strong>Node/UI element</strong>: UI element instances within apps/games, namely UI</li>
<li><strong>query expression</strong>: a serializable data structure through which poco interacts with <strong>target devices</strong> and selects the corresponding UI elements. Tester usually don't need to pay attention to the internal structure of this expression unless they need to customize the <code class="docutils literal"><span class="pre">Selector</span></code> class.</li>
</ul>
<p><img alt="image" src="../_images/hunter-inspector.png" />
<img alt="image" src="../_images/hunter-inspector-text-attribute.png" />
<img alt="image" src="../_images/hunter-inspector-hierarchy-relations.png" /></p>
<div class="section" id="definitions-of-coordinate-system-and-metric-space">
<span id="definitions-of-coordinate-system-and-metric-space"></span><h3>Definitions of coordinate system and metric space<a class="headerlink" href="#definitions-of-coordinate-system-and-metric-space" title="Permalink to this headline">¶</a></h3>
<p><img alt="image" src="../_images/hunter-poco-coordinate-system.png" /></p>
<div class="section" id="normalized-coordinate-system">
<span id="normalized-coordinate-system"></span><h4>Normalized Coordinate System<a class="headerlink" href="#normalized-coordinate-system" title="Permalink to this headline">¶</a></h4>
<p>In normalized coordinate system, the height and width of the screen are measured in the range of 1 unit and these two parameters of UI within poco correspond to certain percentage of the screen size. Hence the same UI on devices with different resolution will have same position and size within normalized coordinate system, which is very helpful to write cross-device test cases.</p>
<p>The space of normalized coordinate system is well distributed. By all means, the coordinate of the screen center is (0.5, 0.5) and the computing method of other scalars and vectors are the same as that of Euclidean space.</p>
</div>
<div class="section" id="local-coordinate-system-local-positioning">
<span id="local-coordinate-system-local-positioning"></span><h4>Local Coordinate System (local positioning)<a class="headerlink" href="#local-coordinate-system-local-positioning" title="Permalink to this headline">¶</a></h4>
<p>The aim of introducing local coordinate system is to express coordinates with reference to a certain UI. Local coordinate system  takes the top left corner  of UI bounding box as origin, the horizontal rightward as x-axis and the vertical downward as y-axis, with the height and width of the bounding box being 1 unit  and other definitions being similar with normalized  coordinate system.</p>
<p>Local coordinate system is more flexible to be used to locate the position within or out of UI. For instance, the coordinate (0.5, 0.5)corresponds to the center of the UI while coordinates larger than 1 or less than 0 correspond to the position out of the UI.</p>
</div>
</div>
</div>
<div class="section" id="poco-instance">
<span id="poco-instance"></span><h2>Poco Instance<a class="headerlink" href="#poco-instance" title="Permalink to this headline">¶</a></h2>
<p>For different engines, please initialize different <code class="docutils literal"><span class="pre">poco</span></code> instance. This part will take Unity3D as an example. For other engines, please refer to:</p>
<ul class="simple">
<li><a class="reference external" href="#">cocos2dx-js</a></li>
<li><a class="reference external" href="#">android-native</a></li>
<li>unreal (in development)</li>
<li>(others see <a class="reference external" href="#">INTEGRATION guide</a> for more details)</li>
</ul>
<div class="highlight-python"><div class="highlight"><pre><span></span><span class="kn">from</span> <span class="nn">poco.vendor.unity3d</span> <span class="kn">import</span> <span class="n">UnityPoco</span>

<span class="n">poco</span> <span class="o">=</span> <span class="n">UnityPoco</span><span class="p">()</span>
<span class="n">ui</span> <span class="o">=</span> <span class="n">poco</span><span class="p">(</span><span class="s1">&#39;...&#39;</span><span class="p">)</span>
</pre></div>
</div>
</div>
<div class="section" id="object-selection-and-operation">
<span id="object-selection-and-operation"></span><h2>Object Selection and Operation<a class="headerlink" href="#object-selection-and-operation" title="Permalink to this headline">¶</a></h2>
<div class="section" id="basic-selector">
<span id="basic-selector"></span><h3>Basic Selector<a class="headerlink" href="#basic-selector" title="Permalink to this headline">¶</a></h3>
<p>The invocation <code class="docutils literal"><span class="pre">poco(...)</span></code> instance is to traverse through the render tree structure and select all the UI elements matching given query expression. The first argument is node name and other key word arguments are correspond to other properties of node. For more information, please refer to API Reference.</p>
<div class="highlight-python"><div class="highlight"><pre><span></span><span class="c1"># select by node name</span>
<span class="n">poco</span><span class="p">(</span><span class="s1">&#39;bg_mission&#39;</span><span class="p">)</span>

<span class="c1"># select by name and other properties</span>
<span class="n">poco</span><span class="p">(</span><span class="s1">&#39;bg_mission&#39;</span><span class="p">,</span> <span class="nb">type</span><span class="o">=</span><span class="s1">&#39;Button&#39;</span><span class="p">)</span>
<span class="n">poco</span><span class="p">(</span><span class="n">textMatches</span><span class="o">=</span><span class="s1">&#39;^据点.*$&#39;</span><span class="p">,</span> <span class="nb">type</span><span class="o">=</span><span class="s1">&#39;Button&#39;</span><span class="p">,</span> <span class="n">enable</span><span class="o">=</span><span class="bp">True</span><span class="p">)</span>
</pre></div>
</div>
<p><img alt="image" src="../_images/hunter-poco-select-simple.png" /></p>
</div>
<div class="section" id="relative-selector">
<span id="relative-selector"></span><h3>Relative Selector<a class="headerlink" href="#relative-selector" title="Permalink to this headline">¶</a></h3>
<p>When there is an ambiguity in the objects selected by node names/node types or failing to select objects, try selecting by hierarchy in a corresponding manner</p>
<div class="highlight-python"><div class="highlight"><pre><span></span><span class="c1"># select by direct child/offspring</span>
<span class="n">poco</span><span class="p">(</span><span class="s1">&#39;main_node&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">child</span><span class="p">(</span><span class="s1">&#39;list_item&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">offspring</span><span class="p">(</span><span class="s1">&#39;item&#39;</span><span class="p">)</span>
</pre></div>
</div>
<p><img alt="image" src="../_images/hunter-poco-select-relative.png" /></p>
</div>
<div class="section" id="sequence-selector-index-selector-iterator-is-more-recommended-for-use">
<span id="sequence-selector-index-selector-iterator-is-more-recommended-for-use"></span><h3>Sequence Selector (index selector, iterator is more recommended for use)<a class="headerlink" href="#sequence-selector-index-selector-iterator-is-more-recommended-for-use" title="Permalink to this headline">¶</a></h3>
<p>Index and traversal will be performed in default up-down or left-right space orders. If the not-yet-traversed nodes are removed from the screen, an exception will be thrown whereas this is not the case for traversed nodes that are removed. As the traversal order has been determined before in advance, the traversal will be performed in a previous order even though the nodes in views are rearranged during the traversal process.</p>
<div class="highlight-python"><div class="highlight"><pre><span></span><span class="n">items</span> <span class="o">=</span> <span class="n">poco</span><span class="p">(</span><span class="s1">&#39;main_node&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">child</span><span class="p">(</span><span class="s1">&#39;list_item&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">offspring</span><span class="p">(</span><span class="s1">&#39;item&#39;</span><span class="p">)</span>
<span class="k">print</span><span class="p">(</span><span class="n">items</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span><span class="o">.</span><span class="n">child</span><span class="p">(</span><span class="s1">&#39;material_name&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">get_text</span><span class="p">())</span>
<span class="k">print</span><span class="p">(</span><span class="n">items</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span><span class="o">.</span><span class="n">child</span><span class="p">(</span><span class="s1">&#39;material_name&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">get_text</span><span class="p">())</span>
</pre></div>
</div>
<p><img alt="image" src="../_images/hunter-poco-select-sequence.png" /></p>
</div>
<div class="section" id="iterate-over-a-collection-of-objects">
<span id="iterate-over-a-collection-of-objects"></span><h3>Iterate over a collection of objects<a class="headerlink" href="#iterate-over-a-collection-of-objects" title="Permalink to this headline">¶</a></h3>
<div class="highlight-python"><div class="highlight"><pre><span></span><span class="c1"># traverse through every item</span>
<span class="n">items</span> <span class="o">=</span> <span class="n">poco</span><span class="p">(</span><span class="s1">&#39;main_node&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">child</span><span class="p">(</span><span class="s1">&#39;list_item&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">offspring</span><span class="p">(</span><span class="s1">&#39;item&#39;</span><span class="p">)</span>
<span class="k">for</span> <span class="n">item</span> <span class="ow">in</span> <span class="n">items</span><span class="p">:</span>
    <span class="n">item</span><span class="o">.</span><span class="n">child</span><span class="p">(</span><span class="s1">&#39;icn_item&#39;</span><span class="p">)</span>
</pre></div>
</div>
<p><img alt="image" src="../_images/hunter-poco-iteration.png" /></p>
</div>
<div class="section" id="get-object-properties">
<span id="get-object-properties"></span><h3>Get object properties<a class="headerlink" href="#get-object-properties" title="Permalink to this headline">¶</a></h3>
<div class="highlight-python"><div class="highlight"><pre><span></span><span class="n">mission_btn</span> <span class="o">=</span> <span class="n">poco</span><span class="p">(</span><span class="s1">&#39;bg_mission&#39;</span><span class="p">)</span>
<span class="k">print</span><span class="p">(</span><span class="n">mission_btn</span><span class="o">.</span><span class="n">attr</span><span class="p">(</span><span class="s1">&#39;type&#39;</span><span class="p">))</span>  <span class="c1"># &#39;Button&#39;</span>
<span class="k">print</span><span class="p">(</span><span class="n">mission_btn</span><span class="o">.</span><span class="n">get_text</span><span class="p">())</span>  <span class="c1"># &#39;据点支援&#39;</span>
<span class="k">print</span><span class="p">(</span><span class="n">mission_btn</span><span class="o">.</span><span class="n">attr</span><span class="p">(</span><span class="s1">&#39;text&#39;</span><span class="p">))</span>  <span class="c1"># &#39;据点支援&#39; equivalent to .get_text()</span>
<span class="k">print</span><span class="p">(</span><span class="n">mission_btn</span><span class="o">.</span><span class="n">exists</span><span class="p">())</span>  <span class="c1"># True/False, exists in the screen or not</span>
</pre></div>
</div>
</div>
<div class="section" id="object-proxy-related-operation">
<span id="object-proxy-related-operation"></span><h3>Object Proxy Related Operation<a class="headerlink" href="#object-proxy-related-operation" title="Permalink to this headline">¶</a></h3>
<div class="section" id="click">
<span id="click"></span><h4>click<a class="headerlink" href="#click" title="Permalink to this headline">¶</a></h4>
<p>The anchorPoint of UI element defaults to the click point. When the first argument is passed to the relative click position, the coordinate of the top-left corner of the bounding box will be <code class="docutils literal"><span class="pre">[0,</span> <span class="pre">0]</span></code> and the bottom right corner <code class="docutils literal"><span class="pre">[1,</span> <span class="pre">1]</span></code>. The deviation range can be less than 0 or larger than 1 and if it turns out to be out of 0~1, that means it is beyond the bounding box.</p>
<div class="highlight-python"><div class="highlight"><pre><span></span><span class="n">poco</span><span class="p">(</span><span class="s1">&#39;bg_mission&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">click</span><span class="p">()</span>
<span class="n">poco</span><span class="p">(</span><span class="s1">&#39;bg_mission&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">click</span><span class="p">(</span><span class="s1">&#39;center&#39;</span><span class="p">)</span>
<span class="n">poco</span><span class="p">(</span><span class="s1">&#39;bg_mission&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">click</span><span class="p">([</span><span class="mf">0.5</span><span class="p">,</span> <span class="mf">0.5</span><span class="p">])</span>    <span class="c1"># equivalent to center</span>
<span class="n">poco</span><span class="p">(</span><span class="s1">&#39;bg_mission&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">focus</span><span class="p">([</span><span class="mf">0.5</span><span class="p">,</span> <span class="mf">0.5</span><span class="p">])</span><span class="o">.</span><span class="n">click</span><span class="p">()</span>  <span class="c1"># equivalent to above expression</span>
</pre></div>
</div>
<p><img alt="image" src="../_images/hunter-poco-click.png" /></p>
</div>
<div class="section" id="swipe">
<span id="swipe"></span><h4>swipe<a class="headerlink" href="#swipe" title="Permalink to this headline">¶</a></h4>
<p>Take the anchor of UI element as origin and swipe a certain distance towards a direction</p>
<div class="highlight-python"><div class="highlight"><pre><span></span><span class="n">joystick</span> <span class="o">=</span> <span class="n">poco</span><span class="p">(</span><span class="s1">&#39;movetouch_panel&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">child</span><span class="p">(</span><span class="s1">&#39;point_img&#39;</span><span class="p">)</span>
<span class="n">joystick</span><span class="o">.</span><span class="n">swipe</span><span class="p">(</span><span class="s1">&#39;up&#39;</span><span class="p">)</span>
<span class="n">joystick</span><span class="o">.</span><span class="n">swipe</span><span class="p">([</span><span class="mf">0.2</span><span class="p">,</span> <span class="o">-</span><span class="mf">0.2</span><span class="p">])</span>  <span class="c1"># swipe sqrt(0.08) unit distance at 45 degree angle up-and-right</span>
<span class="n">joystick</span><span class="o">.</span><span class="n">swipe</span><span class="p">([</span><span class="mf">0.2</span><span class="p">,</span> <span class="o">-</span><span class="mf">0.2</span><span class="p">],</span> <span class="n">duration</span><span class="o">=</span><span class="mf">0.5</span><span class="p">)</span>
</pre></div>
</div>
<p><img alt="image" src="../_images/hunter-poco-swipe.png" /></p>
</div>
<div class="section" id="drag">
<span id="drag"></span><h4>drag<a class="headerlink" href="#drag" title="Permalink to this headline">¶</a></h4>
<p>Drag to target UI from current UI</p>
<div class="highlight-python"><div class="highlight"><pre><span></span><span class="n">poco</span><span class="p">(</span><span class="n">text</span><span class="o">=</span><span class="s1">&#39;突破芯片&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">drag_to</span><span class="p">(</span><span class="n">poco</span><span class="p">(</span><span class="n">text</span><span class="o">=</span><span class="s1">&#39;岩石司康饼&#39;</span><span class="p">))</span>
</pre></div>
</div>
<p><img alt="image" src="../_images/hunter-poco-drag.png" /></p>
</div>
<div class="section" id="focus-local-positioning">
<span id="focus-local-positioning"></span><h4>focus (local positioning)<a class="headerlink" href="#focus-local-positioning" title="Permalink to this headline">¶</a></h4>
<p>The origin defaults to anchor when conducting operations related to node coordinates. Therefore click the anchor directly. If local click deviation is needed, focus can be used. Similar with screen coordinate system, focus takes the upper left corner of bounding box as the origin with the length and width measuring 1, the coordinate of the center being <code class="docutils literal"><span class="pre">[0.5,</span> <span class="pre">0.5]</span></code>, the bottom right corner<code class="docutils literal"><span class="pre">[1,</span> <span class="pre">1]</span></code>, and so on.</p>
<div class="highlight-python"><div class="highlight"><pre><span></span><span class="n">poco</span><span class="p">(</span><span class="s1">&#39;bg_mission&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">focus</span><span class="p">(</span><span class="s1">&#39;center&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">click</span><span class="p">()</span>  <span class="c1"># click the center</span>
</pre></div>
</div>
<p>focus can also be used as internal positioning within an objects, as instanced by the example of implementing a scroll operation in ScrollView</p>
<div class="highlight-python"><div class="highlight"><pre><span></span><span class="n">scrollView</span> <span class="o">=</span> <span class="n">poco</span><span class="p">(</span><span class="nb">type</span><span class="o">=</span><span class="s1">&#39;ScollView&#39;</span><span class="p">)</span>
<span class="n">scrollView</span><span class="o">.</span><span class="n">focus</span><span class="p">([</span><span class="mf">0.5</span><span class="p">,</span> <span class="mf">0.8</span><span class="p">])</span><span class="o">.</span><span class="n">drag_to</span><span class="p">(</span><span class="n">scrollView</span><span class="o">.</span><span class="n">focus</span><span class="p">([</span><span class="mf">0.5</span><span class="p">,</span> <span class="mf">0.2</span><span class="p">]))</span>
</pre></div>
</div>
</div>
<div class="section" id="wait">
<span id="wait"></span><h4>wait<a class="headerlink" href="#wait" title="Permalink to this headline">¶</a></h4>
<p>Wait for the target object to appear and always return  the object itself. If it appears, return it immediately, otherwise, return after timeout</p>
<div class="highlight-python"><div class="highlight"><pre><span></span><span class="n">poco</span><span class="p">(</span><span class="s1">&#39;bg_mission&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">wait</span><span class="p">(</span><span class="mi">5</span><span class="p">)</span><span class="o">.</span><span class="n">click</span><span class="p">()</span>  <span class="c1"># wait 5 seconds at most，click once the object appears</span>
<span class="n">poco</span><span class="p">(</span><span class="s1">&#39;bg_mission&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">wait</span><span class="p">(</span><span class="mi">5</span><span class="p">)</span><span class="o">.</span><span class="n">exists</span><span class="p">()</span>  <span class="c1"># wait 5 seconds at most，return Exists or Not Exists</span>
</pre></div>
</div>
</div>
</div>
<div class="section" id="global-operation">
<span id="global-operation"></span><h3>Global Operation<a class="headerlink" href="#global-operation" title="Permalink to this headline">¶</a></h3>
<p>Can also perform a global operation without any UI elements selected.</p>
<div class="section" id="click">
<span id="id1"></span><h4>click<a class="headerlink" href="#click" title="Permalink to this headline">¶</a></h4>
<div class="highlight-python"><div class="highlight"><pre><span></span><span class="n">poco</span><span class="o">.</span><span class="n">click</span><span class="p">([</span><span class="mf">0.5</span><span class="p">,</span> <span class="mf">0.5</span><span class="p">])</span>  <span class="c1"># click the center of screen</span>
<span class="n">poco</span><span class="o">.</span><span class="n">long_click</span><span class="p">([</span><span class="mf">0.5</span><span class="p">,</span> <span class="mf">0.5</span><span class="p">],</span> <span class="n">duration</span><span class="o">=</span><span class="mi">3</span><span class="p">)</span>
</pre></div>
</div>
</div>
<div class="section" id="swipe">
<span id="id2"></span><h4>swipe<a class="headerlink" href="#swipe" title="Permalink to this headline">¶</a></h4>
<div class="highlight-python"><div class="highlight"><pre><span></span><span class="c1"># swipe from A to B</span>
<span class="n">point_a</span> <span class="o">=</span> <span class="p">[</span><span class="mf">0.1</span><span class="p">,</span> <span class="mf">0.1</span><span class="p">]</span>
<span class="n">center</span> <span class="o">=</span> <span class="p">[</span><span class="mf">0.5</span><span class="p">,</span> <span class="mf">0.5</span><span class="p">]</span>
<span class="n">poco</span><span class="o">.</span><span class="n">swipe</span><span class="p">(</span><span class="n">point_a</span><span class="p">,</span> <span class="n">center</span><span class="p">)</span>

<span class="c1"># swipe from A by given direction</span>
<span class="n">direction</span> <span class="o">=</span> <span class="p">[</span><span class="mf">0.1</span><span class="p">,</span> <span class="mi">0</span><span class="p">]</span>
<span class="n">poco</span><span class="o">.</span><span class="n">swipe</span><span class="p">(</span><span class="n">point_a</span><span class="p">,</span> <span class="n">direction</span><span class="o">=</span><span class="n">direction</span><span class="p">)</span>
</pre></div>
</div>
</div>
<div class="section" id="snapshot">
<span id="snapshot"></span><h4>snapshot<a class="headerlink" href="#snapshot" title="Permalink to this headline">¶</a></h4>
<p>Take a screenshot of the current screen and save it to file.</p>
<p><strong>Note</strong>: <code class="docutils literal"><span class="pre">snapshot</span></code> does not support in some engine implementation of poco.</p>
<div class="highlight-python"><div class="highlight"><pre><span></span><span class="kn">from</span> <span class="nn">base64</span> <span class="kn">import</span> <span class="n">b64decode</span>

<span class="n">b64img</span> <span class="o">=</span> <span class="n">poco</span><span class="o">.</span><span class="n">snapshot</span><span class="p">(</span><span class="n">width</span><span class="o">=</span><span class="mi">720</span><span class="p">)</span>
<span class="nb">open</span><span class="p">(</span><span class="s1">&#39;screen.png&#39;</span><span class="p">,</span> <span class="s1">&#39;wb&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">write</span><span class="p">(</span><span class="n">b64decode</span><span class="p">(</span><span class="n">b64img</span><span class="p">))</span>
</pre></div>
</div>
</div>
</div>
</div>
<div class="section" id="exceptions">
<span id="exceptions"></span><h2>Exceptions<a class="headerlink" href="#exceptions" title="Permalink to this headline">¶</a></h2>
<div class="section" id="pocotargettimeout">
<span id="pocotargettimeout"></span><h3>PocoTargetTimeout<a class="headerlink" href="#pocotargettimeout" title="Permalink to this headline">¶</a></h3>
<div class="highlight-python"><div class="highlight"><pre><span></span><span class="kn">from</span> <span class="nn">poco.exceptions</span> <span class="kn">import</span> <span class="n">PocoTargetTimeout</span>

<span class="k">try</span><span class="p">:</span>
    <span class="n">poco</span><span class="p">(</span><span class="s1">&#39;guide_panel&#39;</span><span class="p">,</span> <span class="nb">type</span><span class="o">=</span><span class="s1">&#39;ImageView&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">wait_for_appearance</span><span class="p">()</span>
<span class="k">except</span> <span class="n">PocoTargetTimeout</span><span class="p">:</span>
    <span class="c1"># bugs here as the panel not shown</span>
    <span class="k">raise</span>
</pre></div>
</div>
</div>
<div class="section" id="poconosuchnodeexception">
<span id="poconosuchnodeexception"></span><h3>PocoNoSuchNodeException<a class="headerlink" href="#poconosuchnodeexception" title="Permalink to this headline">¶</a></h3>
<div class="highlight-python"><div class="highlight"><pre><span></span><span class="kn">from</span> <span class="nn">poco.exceptions</span> <span class="kn">import</span> <span class="n">PocoNoSuchNodeException</span>

<span class="n">img</span> <span class="o">=</span> <span class="n">poco</span><span class="p">(</span><span class="s1">&#39;guide_panel&#39;</span><span class="p">,</span> <span class="nb">type</span><span class="o">=</span><span class="s1">&#39;ImageView&#39;</span><span class="p">)</span>
<span class="k">try</span><span class="p">:</span>
    <span class="k">if</span> <span class="ow">not</span> <span class="n">img</span><span class="o">.</span><span class="n">exists</span><span class="p">():</span>
        <span class="n">img</span><span class="o">.</span><span class="n">click</span><span class="p">()</span>
<span class="k">except</span> <span class="n">PocoNoSuchNodeException</span><span class="p">:</span>
    <span class="c1"># If attempt to operate inexistent nodes, an exception will be thrown</span>
    <span class="k">pass</span>
</pre></div>
</div>
</div>
</div>
<div class="section" id="unit-test">
<span id="unit-test"></span><h2>Unit Test<a class="headerlink" href="#unit-test" title="Permalink to this headline">¶</a></h2>
<p>poco is an automation framework. For unit testing, please refer to <a class="reference external" href="http://git-qa.gz.netease.com/maki/PocoUnit">PocoUnit</a>. PocoUnit provides a full set of assertion methods and it is compatible with the unittest in python standard library.</p>
</div>
</div>


           </div>
           <div class="articleComments">
            
           </div>
          </div>
          <footer>
  
    <div class="rst-footer-buttons" role="navigation" aria-label="footer navigation">
      
        <a href="poco.html" class="btn btn-neutral float-right" title="poco package" accesskey="n" rel="next">Next <span class="fa fa-arrow-circle-right"></span></a>
      
      
        <a href="../index.html" class="btn btn-neutral" title="Welcome to Poco’s documentation!" accesskey="p" rel="prev"><span class="fa fa-arrow-circle-left"></span> Previous</a>
      
    </div>
  

  <hr/>

  <div role="contentinfo">
    <p>
        &copy; Copyright 2017, NetEase Co, Ltd..

    </p>
  </div>
  Built with <a href="http://sphinx-doc.org/">Sphinx</a> using a <a href="https://github.com/snide/sphinx_rtd_theme">theme</a> provided by <a href="https://readthedocs.org">Read the Docs</a>. 

</footer>

        </div>
      </div>

    </section>

  </div>
  


  

    <script type="text/javascript">
        var DOCUMENTATION_OPTIONS = {
            URL_ROOT:'../',
            VERSION:'',
            COLLAPSE_INDEX:false,
            FILE_SUFFIX:'.html',
            HAS_SOURCE:  true,
            SOURCELINK_SUFFIX: '.txt'
        };
    </script>
      <script type="text/javascript" src="../_static/jquery.js"></script>
      <script type="text/javascript" src="../_static/underscore.js"></script>
      <script type="text/javascript" src="../_static/doctools.js"></script>

  

  
  
    <script type="text/javascript" src="../_static/js/theme.js"></script>
  

  
  
  <script type="text/javascript">
      jQuery(function () {
          SphinxRtdTheme.StickyNav.enable();
      });
  </script>
   

</body>
</html>